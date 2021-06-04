import Prism from "prismjs"
import { useEffect } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'
import StackElement from './StackElement.js'

const Stack = ({stack, sendCommand}) => {
    console.log(stack)
    return (
        <div className="section">
            <div className="section-title">Stack</div>
            <div className="scrollable">
                <div className="stack">
                    {stack.stack.map((ele) => {
                        return <StackElement key={ele.idx} active={stack.curr} info={ele} sendCommand={sendCommand}/>
                    })}
                </div>
            </div>
        </div>
    )
}

export default Stack; 