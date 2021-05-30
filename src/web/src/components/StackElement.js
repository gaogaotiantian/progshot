import Prism from "prismjs"
import { useEffect } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'

const StackElement = ({active, info, sendCommand}) => {
    useEffect(() => {
        Prism.highlightAll();
    })

    const cls = () => {
            if (active === info.idx) {
                return "active-stack"
            } else {
                return ""
            }
        };
    return (
        <div className={"mono-word stack-element " + cls()} onClick={() => sendCommand("j " + info.idx.toString(), "command")}>
            {info.file_string + "\n" + info.code_string + "\n"}
        </div>
    )
}

export default StackElement; 