// Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
// For details: https://github.com/gaogaotiantian/progshot/blob/master/NOTICE.txt


import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'

const StackElement = ({active, info, sendCommand}) => {

    const cls = () => {
            if (active === info.idx) {
                return "active-stack"
            } else {
                return ""
            }
        };

    return (
        <div className={"mono-word stack-element " + cls()} onClick={() => sendCommand("frame " + info.idx.toString(), "command")}>
            {info.file_string + "\n > " + info.code_string + "\n"}
        </div>
    )
}

export default StackElement; 
