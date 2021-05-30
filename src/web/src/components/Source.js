import Prism from "prismjs"
import { useEffect } from "react";
import "../prism.css";
import '../App.css';
import 'prismjs/components/prism-python'
import 'prismjs/plugins/line-numbers/prism-line-numbers'
import 'prismjs/plugins/line-highlight/prism-line-highlight'
import SourceTitle from './SourceTitle.js'

Prism.manual = true;
const Source = ({currSource, currFilm, setCurrFilm, sendCommand}) => {
    useEffect(() => {
        Prism.highlightAll();
    })

    return (
        <div className="section">
            <div className="source-grid">
                <SourceTitle filmInfo={currSource.film} currFilm={currFilm} setCurrFilm={setCurrFilm} sendCommand={sendCommand}/>
                <pre className="line-numbers source" data-line={currSource.curr_lineno}>
                    <code className="language-py">{currSource.code}</code>
                </pre>
            </div>
        </div>
    )
}

export default Source; 