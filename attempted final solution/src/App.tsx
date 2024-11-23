import { ReactFlow } from '@xyflow/react';
import { Slide, SLIDE_WIDTH } from './slide.tsx';
 
const nodeTypes = {
    slide: Slide,
};
 
export default function App() {
  const nodes = [
    {
        id: '0',
        type: 'slide',
        position: { x: 0, y: 0 },
        data: { source: '# Hello, React Flow!' },
      },
      {
        id: '1',
        type: 'slide',
        position: { x: SLIDE_WIDTH, y: 0 },
        data: { source: '...' },
      },
      {
        id: '2',
        type: 'slide',
        position: { x: SLIDE_WIDTH * 2, y: 0 },
        data: { source: '...' },
      },
  ];
 
  return <ReactFlow 
  nodes={nodes} 
  nodeTypes={nodeTypes} 
  fitView 
  minZoom={0.1}/>;
}