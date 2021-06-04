import Prism from "prismjs"
import { useEffect, useRef} from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/plugins/line-highlight/prism-line-highlight'
import SourceTitle from './SourceTitle.js'

Prism.manual = true;
const Source = ({currSource, currFilm, setCurrFilm, sendCommand}) => {
    const code = useRef(null);
    useEffect(() => {
        Prism.highlightAllUnder(code.current);
    })

    return (
        <div className="section">
            <SourceTitle filmInfo={currSource.film} currFilm={currFilm} setCurrFilm={setCurrFilm} sendCommand={sendCommand}/>
            <div className="scrollable">
                <pre ref={code} id="source-code" className="line-numbers source" data-line={currSource.curr_lineno}>
                    <code className="source-code language-py">{currSource.code}</code>
                </pre>
            </div>
        </div>
    )
}

export default Source; 
