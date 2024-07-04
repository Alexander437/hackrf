import { interpolateRgb } from 'd3-interpolate';
import 'tailwindcss/tailwind.css';

function Heatmap(props) {
    const { data } = props

    const numRows = data.length;
    const numCols = data[0].length;
    const squareWidth = 128 / numCols; // Ширина квадрата
    const squareHeight = 20 / numRows; // Высота квадрата

    const flatValues = data.flat();
    const minVal = Math.min(...flatValues);
    const maxVal = Math.max(...flatValues);

    // Интерполяция цветов от оранжевого до фиолетового
    const interpolateWarm = interpolateRgb('orange', 'purple');

    const colorScale = (value) => {
        const normalizedValue = (value - minVal) / (maxVal - minVal);
        return interpolateWarm(normalizedValue);
    };

    const squares = data.flatMap((row, rowIndex) =>
        row.map((value, colIndex) => {
            const color = colorScale(value);
            return (
                <rect
                    key={`${rowIndex}-${colIndex}`}
                    x={colIndex * squareWidth}
                    y={rowIndex * squareHeight}
                    width={squareWidth}
                    height={squareHeight}
                    fill={color}
                />
            );
        })
    );

    return (
        <svg className="max-w-full h-auto" viewBox={`0 0 128 20`}>
            {squares}
        </svg>
    );
}

export default Heatmap