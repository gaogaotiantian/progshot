import Prism from "prismjs"
import { useEffect, useState } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'
import 'prismjs/plugins/command-line/prism-command-line'

const Terminal = ({sendCommand, addToConsoleHistory, consoleHistory, consoleOutputLines}) => {
    const [command, setCommand] = useState("")

    useEffect(() => {
        Prism.highlightAll();
    })

    const handleKeyDown = async (event) => {
        if (event.key === 'Enter') {
            addToConsoleHistory(command + "\n", false)
            if (command !== "") {
                sendCommand(command, "console")
            }
            setCommand("")
        }
    }

    return (
        <div className="section">
            <div className="grid">
                <div className="section-title">Terminal</div>
                    <pre className="command-line terminal" data-host="psviewer" data-output={consoleOutputLines}>
                        <code className="language-py">{consoleHistory}</code>
                        <input className="mono-word terminal-input" type="text" id="input" value={command} onChange={(e) => {setCommand(e.target.value)}} onKeyDown={(e) => handleKeyDown(e)}/>
                    </pre>
            </div>
        </div>
    )
}

export default Terminal; 