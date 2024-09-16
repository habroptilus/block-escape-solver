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

  // マス目のクリック処理
  const handleCellClick = (y: number, x: number) => {
    setSelectedPosition({ y, x });
  };

  // ブロックが現在のセルに存在するかチェック
  const isBlockAtPosition = (y: number, x: number) => {
    for (const block of blocks) {
      if (block.orientation === "H") {
        if (block.position.y === y && block.position.x <= x && x < block.position.x + block.length) {
          return block;
        }
      } else if (block.orientation === "V") {
        if (block.position.x === x && block.position.y <= y && y < block.position.y + block.length) {
          return block;
        }
      }
    }
    return null;
  };

  // ボードの描画
  const renderBoard = () => {
    return initialBoard.map((row, y) => (
      <div key={y} style={{ display: "flex" }}>
        {row.map((cell, x) => {
          const block = isBlockAtPosition(y, x);
          return (
            <div
              key={x}
              onClick={() => handleCellClick(y, x)}
              style={{
                width: "50px",
                height: "50px",
                border: "1px solid black",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: block
                  ? block.isTarget
                    ? "lightcoral"
                    : "lightgray"
                  : selectedPosition?.y === y && selectedPosition?.x === x
                  ? "lightblue"
                  : "white",
              }}
            >
              {/* ゴールの表示 */}
              {y === 2 && x === 5 && !block ? "G" : ""}
            </div>
          );
        })}
      </div>
    ));
  };

  return (
    <div>
      <h1>Block Escape Solver</h1>
      
      <h2>Board</h2>
      {renderBoard()}

      <h2>Create Block</h2>
      <div>
        <label>
          Orientation:
          <select
            value={blockOrientation}
            onChange={(e) => setBlockOrientation(e.target.value as Orientation)}
          >
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
          Is Target Block:
          <input
            type="checkbox"
            checked={isTargetBlock}
            onChange={(e) => setIsTargetBlock(e.target.checked)}
          />
        </label>

        <button onClick={createBlock}>Create Block</button>
      </div>
    </div>
  );
};

export default Page;
