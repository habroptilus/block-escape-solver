// app/solve/page.tsx
"use client";

import React, { useState } from "react";

type Orientation = "H" | "V";

interface Block {
  id: number;
  orientation: Orientation;
  length: number;
  isTarget: boolean;
  position: { y: number; x: number };
}

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

  // ブロック作成
  const createBlock = () => {
    if (!selectedPosition) {
      alert("Please select a position on the board to place the block.");
      return;
    }

    // ブロックの範囲が盤面を超えないかチェック
    if (
      (blockOrientation === "H" && selectedPosition.x + blockLength > 6) ||
      (blockOrientation === "V" && selectedPosition.y + blockLength > 6)
    ) {
      alert("Block is out of bounds!");
      return;
    }

    // 重複ブロックチェック
    for (const block of blocks) {
      if (block.orientation === "H") {
        if (
          block.position.y === selectedPosition.y &&
          !(block.position.x + block.length <= selectedPosition.x || block.position.x >= selectedPosition.x + blockLength)
        ) {
          setErrorMessage("Block overlaps with an existing block.");
          return;
        }
      } else if (block.orientation === "V") {
        if (
          block.position.x === selectedPosition.x &&
          !(block.position.y + block.length <= selectedPosition.y || block.position.y >= selectedPosition.y + blockLength)
        ) {
          setErrorMessage("Block overlaps with an existing block.");
          return;
        }
      }
    }

    setErrorMessage(null); // エラーメッセージリセット

    const newBlock: Block = {
      id: blockIdCounter,
      orientation: blockOrientation,
      length: blockLength,
      isTarget: isTargetBlock,
      position: selectedPosition,
    };

    setBlocks((prevBlocks) => [...prevBlocks, newBlock]);
    setBlockIdCounter((prevCounter) => prevCounter + 1);
    setSelectedPosition(null); // リセット
  };

  return (
    <div>
      <h1>Block Placement</h1>
      <div>
        <label>
          Orientation:
          <select value={blockOrientation} onChange={(e) => setBlockOrientation(e.target.value as Orientation)}>
            <option value="H">Horizontal</option>
            <option value="V">Vertical</option>
          </select>
        </label>
        <label>
          Length:
          <select value={blockLength} onChange={(e) => setBlockLength(Number(e.target.value))}>
            <option value={2}>2</option>
            <option value={3}>3</option>
          </select>
        </label>
        <label>
          Target:
          <input type="checkbox" checked={isTargetBlock} onChange={(e) => setIsTargetBlock(e.target.checked)} />
        </label>
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
                          border: "none", // borderを削除して重複表示を防ぐ
                        }}
                      />
                    );
                  }

                  return null;
                })}
              </div>
            ))
          )}
        </div>
      </div>
      <button onClick={createBlock}>Create Block</button>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
    </div>
  );
};

export default Page;
