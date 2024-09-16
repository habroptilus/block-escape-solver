"use client";

import React, { useState } from "react";
import SolutionBoard from './SolutionBoard';

type Orientation = "H" | "V";

interface Block {
  id: number;
  orientation: Orientation;
  length: number;
  isTarget: boolean;
  position: { y: number; x: number };
}

type Position = {
  x: number;
  y: number;
};

const isOverlapping = (
  block: Block,
  selectedPosition: Position,
  blockLength: number,
  orientation: 'H' | 'V',
  is_target_block: boolean
): boolean => {
  const selectedBlock: Block = {
    id: 1000, // dummy
    position: selectedPosition,
    length: blockLength,
    orientation: orientation,
    isTarget: is_target_block
  };

  const getBlockRange = (block: Block) => {
    const { x, y } = block.position;
    const length = block.length;
    if (block.orientation === 'H') {
      return {
        left: x,
        right: x + length,
        top: y,
        bottom: y + 1, // 1行分の高さ
      };
    } else {
      return {
        left: x,
        right: x + 1, // 1列分の幅
        top: y,
        bottom: y + length,
      };
    }
  };

  const blockRange = getBlockRange(block);
  const selectedBlockRange = getBlockRange(selectedBlock);

  return !(blockRange.right <= selectedBlockRange.left || 
           blockRange.left >= selectedBlockRange.right || 
           blockRange.bottom <= selectedBlockRange.top || 
           blockRange.top >= selectedBlockRange.bottom);
};

const initialBoard = Array(6)
  .fill(null)
  .map(() => Array(6).fill(null));
const Page = () => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [blockIdCounter, setBlockIdCounter] = useState(0);
  const [blockOrientation, setBlockOrientation] = useState<Orientation>("H");
  const [blockLength, setBlockLength] = useState<number>(2);
  const [isTargetBlock, setIsTargetBlock] = useState<boolean>(false);
  const [selectedPosition, setSelectedPosition] = useState<{ y: number; x: number } | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [solution, setSolution] = useState<any[] | null>(null); // ソリューション表示用の状態

  const createBlock = () => {
    if (!selectedPosition) {
      alert("Please select a position on the board to place the block.");
      return;
    }

    if (
      (blockOrientation === "H" && selectedPosition.x + blockLength > 6) ||
      (blockOrientation === "V" && selectedPosition.y + blockLength > 6)
    ) {
      alert("Block is out of bounds!");
      return;
    }

    for (const block of blocks) {
      if (isOverlapping(block, selectedPosition,  blockLength, blockOrientation, isTargetBlock,)) {
        setErrorMessage("Block overlaps with an existing block.");
        return;
      }
    }

    setErrorMessage(null);

    const newBlock: Block = {
      id: blockIdCounter,
      orientation: blockOrientation,
      length: blockLength,
      isTarget: isTargetBlock,
      position: selectedPosition,
    };

    setBlocks((prevBlocks) => [...prevBlocks, newBlock]);
    setBlockIdCounter((prevCounter) => prevCounter + 1);
    setSelectedPosition(null);
  };

  const removeLastBlock = () => {
    setBlocks((prevBlocks) => prevBlocks.slice(0, -1));
    setBlockIdCounter((prevCounter) => prevCounter - 1);
  };

  const solveBoard = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/solve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          width: 6,
          height: 6,
          goal: { y: 2, x: 5 },
          positions: blocks.map((block) => ({
            block: {
              id: block.id,
              orientation: block.orientation,
              length: block.length,
              is_target: block.isTarget,
            },
            cell: {
              x: block.position.x,
              y: block.position.y,
            },
          })),
        }),
      });
  
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
  
      const data = await response.json();
      setSolution(data.solution);
    } catch (error) {
      setErrorMessage("An error occurred while solving the board.");
    }
  };

  return (
    <div>
      <h1>Block Placement</h1>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          marginBottom: '20px',
          padding: '10px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9',
        }}
      >
        <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        padding: '20px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
        maxWidth: '300px',
      }}
    >
      <label style={{ display: 'flex', flexDirection: 'column' }}>
        <span style={{ marginBottom: '5px', fontWeight: 'bold' }}>Orientation:</span>
        <select
          value={blockOrientation}
          onChange={(e) => setBlockOrientation(e.target.value as Orientation)}
          style={{
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ddd',
          }}
        >
          <option value="H">Horizontal</option>
          <option value="V">Vertical</option>
        </select>
      </label>
      <label style={{ display: 'flex', flexDirection: 'column' }}>
        <span style={{ marginBottom: '5px', fontWeight: 'bold' }}>Length:</span>
        <select
          value={blockLength}
          onChange={(e) => setBlockLength(Number(e.target.value))}
          style={{
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ddd',
          }}
        >
          <option value={2}>2</option>
          <option value={3}>3</option>
        </select>
      </label>
      <label style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ marginRight: '10px', fontWeight: 'bold' }}>Target:</span>
        <input
          type="checkbox"
          checked={isTargetBlock}
          onChange={(e) => setIsTargetBlock(e.target.checked)}
          style={{
            width: '20px',
            height: '20px',
          }}
        />
      </label>
    </div>
        <div
          style={{
            display: 'flex',
            gap: '10px',
            flexDirection: 'row',
            alignItems: 'center',
          }}
        >
          <button
            onClick={createBlock}
            style={{
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              backgroundColor: '#4CAF50', // グリーンの背景色
              color: '#fff', // 白い文字
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#45a049')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#4CAF50')}
          >
            Create Block
          </button>
          <button
            onClick={removeLastBlock}
            style={{
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              backgroundColor: '#f44336', // 赤い背景色
              color: '#fff', // 白い文字
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#e53935')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#f44336')}
          >
            Remove Last Block
          </button>
        </div>
      </div>
      <div>
        <h2>Select Position</h2>
        <div
          style={{
            position: "relative",
            display: "grid",
            gridTemplateColumns: "repeat(6, 40px)",
            gridTemplateRows: "repeat(6, 40px)",
          }}
        >
          {initialBoard.map((row, rowIndex) =>
            row.map((_, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                onClick={() => setSelectedPosition({ y: rowIndex, x: colIndex })}
                style={{
                  width: "40px",
                  height: "40px",
                  border: "1px solid lightgray",
                  backgroundColor: selectedPosition?.x === colIndex && selectedPosition?.y === rowIndex ? "lightblue" : "white",
                  position: "relative",
                }}
              >
                {blocks.map((block) => {
                  const { orientation, length, isTarget, position } = block;
                  const blockCells = [];
                  for (let i = 0; i < length; i++) {
                    if (orientation === "H") {
                      blockCells.push({ y: position.y, x: position.x + i });
                    } else {
                      blockCells.push({ y: position.y + i, x: position.x });
                    }
                  }

                  // 一部のマスのみにブロックが描画されるように修正
                  if (blockCells.some(cell => cell.y === rowIndex && cell.x === colIndex)) {
                    return (
                      <div
                        key={`${block.id}-${rowIndex}-${colIndex}`}
                        style={{
                          position: "absolute",
                          top: "0",
                          left: "0",
                          width: "40px",
                          height: "40px",
                          backgroundColor: isTarget ? "lightcoral" : "lightgray",
                          zIndex: 1,
                          pointerEvents: "none",
                        }}
                      />
                    );
                  }

                  return null;
                })}
                {rowIndex === 2 && colIndex === 5 && (
                  <div
                    style={{
                      position: "absolute",
                      top: "0",
                      left: "0",
                      width: "40px",
                      height: "40px",
                      backgroundColor: "lightgreen",
                      color: "white",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: "bold",
                      zIndex: 2,
                    }}
                  >
                    G
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
      <button
        onClick={solveBoard}
        style={{
          padding: '10px 20px',
          borderRadius: '5px',
          border: 'none',
          backgroundColor: '#2196F3', // 青い背景色
          color: '#fff', // 白い文字
          fontSize: '16px',
          cursor: 'pointer',
          transition: 'background-color 0.3s ease',
          marginTop: '20px',
        }}
        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#1976D2')}
        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#2196F3')}
      >
        Solve
      </button>
      
      {errorMessage && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {errorMessage}
        </div>
      )}
      {solution && <SolutionBoard solution={solution} />}
    </div>
  );
};


export default Page;
