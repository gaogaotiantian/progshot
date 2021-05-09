import Prism from "prismjs"
import { useEffect, useState } from "react";
import '../App.css';
import "../prism.css";
import 'prismjs/components/prism-python'
import 'prismjs/plugins/command-line/prism-command-line'

const Terminal = ({exeCommand}) => {
    const [command, setCommand] = useState("")
    const [history, setHistory] = useState("\n")
    const [console_output_lines, setConsoleOutputLines] = useState("1")
    const [console_line_count, setConsoleLineCount] = useState(1)

    useEffect(() => {
        Prism.highlightAll();
    })

    const handleKeyDown = async (event) => {
        if (event.key === 'Enter') {
            console.log(command)
            var append = command + "\n"
            if (command !== "") {
                console.log("not empty")
                const exeResult = await exeCommand(command)
                if (exeResult !== "") {
                    append += exeResult + "\n"
                    calculateOutputLines(exeResult)
                }
            }
            setHistory(history + append)
            setCommand("")
            setConsoleLineCount(console_line_count + (append.match(/\n/g) || []).length)
        }
    }

    const calculateOutputLines = (output) => {
        const start = console_line_count + 2
        const end = console_line_count + 2 + (output.match(/\n/g) || []).length
        setConsoleOutputLines(console_output_lines + "," + start.toString() + "-" + end.toString())
    }

    return (
        <pre className="command-line column" data-host="psviewer" data-output={console_output_lines}>
            <code className="language-py">{history}</code>
            <input type="text" id="input" value={command} onChange={(e) => {setCommand(e.target.value)}} onKeyDown={(e) => handleKeyDown(e)}/>
        </pre>
    )
}

export default Terminal; 