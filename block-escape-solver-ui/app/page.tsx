"use client";
import { useState, useRef, useEffect } from "react";

const BLOCK_SIZE = 50;
const BOARD_SIZE = 6;
const GOAL_POSITION = { x: 5, y: 2 };

interface Block {
  orientation: "H" | "V";
  length: number;
  isTarget: boolean;
}

interface Position {
  x: number;
  y: number;
  block: Block;
}

const initialBlocks: Block[] = [
  { orientation: "H", length: 2, isTarget: true },
  { orientation: "H", length: 2, isTarget: false },
  { orientation: "V", length: 3, isTarget: false },
  { orientation: "H", length: 3, isTarget: false },
  { orientation: "V", length: 2, isTarget: false },
];

const BlockPuzzle = () => {
  const [blocks, setBlocks] = useState<Position[]>([]);
  const [selectedBlock, setSelectedBlock] = useState<Block | null>(null);
  const [gifUrl, setGifUrl] = useState<string | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    drawGrid();
    drawBlocks();
  }, [blocks]);

  const drawGrid = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "black";
    for (let i = 0; i <= BOARD_SIZE; i++) {
      ctx.beginPath();
      ctx.moveTo(i * BLOCK_SIZE, 0);
      ctx.lineTo(i * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE);
      ctx.stroke();
      ctx.moveTo(0, i * BLOCK_SIZE);
      ctx.lineTo(BOARD_SIZE * BLOCK_SIZE, i * BLOCK_SIZE);
      ctx.stroke();
    }

    ctx.fillStyle = "blue";
    ctx.font = "bold 20px Arial";
    ctx.fillText("G", GOAL_POSITION.x * BLOCK_SIZE + 15, GOAL_POSITION.y * BLOCK_SIZE + 35);
  };

  const drawBlocks = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    blocks.forEach(({ x, y, block }) => {
      ctx.fillStyle = block.isTarget ? "red" : "gray";
      ctx.fillRect(
        x * BLOCK_SIZE,
        y * BLOCK_SIZE,
        block.orientation === "H" ? block.length * BLOCK_SIZE : BLOCK_SIZE,
        block.orientation === "V" ? block.length * BLOCK_SIZE : BLOCK_SIZE
      );
      
      ctx.strokeStyle = "black";
      ctx.lineWidth = 2;
      ctx.strokeRect(
        x * BLOCK_SIZE,
        y * BLOCK_SIZE,
        block.orientation === "H" ? block.length * BLOCK_SIZE : BLOCK_SIZE,
        block.orientation === "V" ? block.length * BLOCK_SIZE : BLOCK_SIZE
      );
    });
  };

  const handleCellClick = (event: React.MouseEvent<HTMLCanvasElement>) => {
    if (!selectedBlock) return;

    if (selectedBlock.isTarget && blocks.some(b => b.block.isTarget)) {
      return; // 既にターゲットブロックが配置されている場合は追加しない
    }

    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    const x = Math.floor((event.clientX - rect.left) / BLOCK_SIZE);
    const y = Math.floor((event.clientY - rect.top) / BLOCK_SIZE);

    if (x < BOARD_SIZE && y < BOARD_SIZE) {
      setBlocks([...blocks, { x, y, block: selectedBlock }]);
    }
  };

  const handleBlockSelect = (block: Block) => {
    setSelectedBlock(block);
  };

  const handleUndo = () => {
    setBlocks((prev) => prev.slice(0, -1));
  };

  const handleReset = () => {
    setBlocks([]);
  };

  const handleSolve = async () => {
    let idCounter = 0;
    const jsonData = {
      width: BOARD_SIZE,
      height: BOARD_SIZE,
      goal: GOAL_POSITION,
      positions: blocks.map(({ x, y, block }) => ({
        cell: { x, y },
        block: {
          id: idCounter++,
          orientation: block.orientation,
          length: block.length,
          is_target: block.isTarget,
        },
      })),
    };

    const response = await fetch("/api/upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
      console.error("Failed to get GIF");
      return;
    }

    const blob = await response.blob();
    setGifUrl(URL.createObjectURL(blob));
  };

  return (
    <div className="flex flex-col items-center">
      <div className="flex gap-2 p-4 border">
        {initialBlocks.map((block, index) => (
          <div
            key={index}
            className={`relative cursor-pointer border border-black ${block.isTarget ? "bg-red-500" : "bg-gray-500"} ${selectedBlock === block ? "border-4 border-blue-500 shadow-lg shadow-blue-500/50 scale-110" : ""}`}
            onClick={() => handleBlockSelect(block)}
            style={{
              width: block.orientation === "H" ? block.length * BLOCK_SIZE : BLOCK_SIZE,
              height: block.orientation === "V" ? block.length * BLOCK_SIZE : BLOCK_SIZE,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              transition: "transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out",
            }}
          ></div>
        ))}
      </div>
      <canvas
        ref={canvasRef}
        width={BOARD_SIZE * BLOCK_SIZE}
        height={BOARD_SIZE * BLOCK_SIZE}
        className="border bg-white mt-4"
        onClick={handleCellClick}
      ></canvas>
      <div className="mt-4 flex gap-4">
        <button onClick={handleUndo} className="px-4 py-2 bg-blue-500 text-white rounded">Undo</button>
        <button onClick={handleReset} className="px-4 py-2 bg-green-500 text-white rounded">Reset Board</button>
        <button onClick={handleSolve} className="px-4 py-2 bg-red-500 text-white rounded">Solve</button>
      </div>
      {gifUrl && <img src={gifUrl} alt="Solution GIF" className="mt-4" />}
    </div>
  );
};

export default BlockPuzzle;