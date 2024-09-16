import React, { useState } from 'react';

type Move = {
  from_cell: { x: number; y: number };
  direction: 'up' | 'down' | 'left' | 'right';
  block_id: number;
};

type Props = {
  solution: Move[];
};

const ArrowSymbol: React.FC<{ direction: 'up' | 'down' | 'left' | 'right' }> = ({ direction }) => {
  const arrowMap = {
    up: '↑',
    down: '↓',
    left: '←',
    right: '→',
  };

  return (
    <span
      style={{
        fontSize: '24px',  // 大きさを変更
        fontWeight: 'bold', // 太さを変更
        color: 'blue',
      }}
    >
      {arrowMap[direction]}
    </span>
  );
};

const SolutionBoard: React.FC<Props> = ({ solution }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const handleNext = () => {
    setCurrentStep((prevStep) => (prevStep < solution.length - 1 ? prevStep + 1 : prevStep));
  };

  const handlePrev = () => {
    setCurrentStep((prevStep) => (prevStep > 0 ? prevStep - 1 : prevStep));
  };

  const gridSize = 6; // 盤面のサイズ
  const cellSize = 40; // 各セルのサイズ

  // 現在のステップに対応する move を取得
  const moveToShow = solution[currentStep];

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ marginBottom: '10px', fontSize: '16px' }}>
          Step {currentStep + 1} / {solution.length}
      </div>
      <div
        style={{
          position: 'relative',
          width: `${gridSize * cellSize}px`,
          height: `${gridSize * cellSize}px`,
          border: '1px solid lightgray',
          display: 'grid',
          gridTemplateColumns: `repeat(${gridSize}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${gridSize}, ${cellSize}px)`,
          margin: '0 auto', // 中央揃え
        }}
      >
        {Array.from({ length: gridSize * gridSize }, (_, index) => {
          const x = index % gridSize;
          const y = Math.floor(index / gridSize);
          return (
            <div
              key={index}
              style={{
                width: `${cellSize}px`,
                height: `${cellSize}px`,
                border: '1px solid lightgray',
                boxSizing: 'border-box',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: (moveToShow.from_cell.x === x && moveToShow.from_cell.y === y) ? 'lightyellow' : 'white',
              }}
            >
              {moveToShow.from_cell.x === x && moveToShow.from_cell.y === y ? (
                <ArrowSymbol direction={moveToShow.direction} />
              ) : null}
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: '10px' }}>
        <button
          onClick={handlePrev}
          disabled={currentStep === 0}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            color: 'white',
            backgroundColor: currentStep === 0 ? 'gray' : 'blue',
            border: 'none',
            borderRadius: '5px',
            cursor: currentStep === 0 ? 'not-allowed' : 'pointer',
            marginRight: '10px',
          }}
        >
          Prev
        </button>
        <button
          onClick={handleNext}
          disabled={currentStep >= solution.length - 1}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            color: 'white',
            backgroundColor: currentStep >= solution.length - 1 ? 'gray' : 'blue',
            border: 'none',
            borderRadius: '5px',
            cursor: currentStep >= solution.length - 1 ? 'not-allowed' : 'pointer',
          }}
        >
          Next
        </button>
        
      </div>
    </div>
  );
};

export default SolutionBoard;
