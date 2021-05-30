import { useState } from "react";
import '../App.css';
import ArrowBackIosSharpIcon from '@material-ui/icons/ArrowBackIosSharp';
import ArrowForwardIosSharpIcon from '@material-ui/icons/ArrowForwardIosSharp';

const SourceTitle = ({filmInfo, currFilm, setCurrFilm, sendCommand}) => {

    return (
        <div className="source-title section-title">
            <div className="film-name">{filmInfo.name}</div>

            <div className="slider-group">
                <input className="slider" type="range" min="1" max={filmInfo.num_films} step="1" value={currFilm}
                    onChange={(e) => setCurrFilm(e.target.value)} onMouseUp={() => sendCommand("g " + currFilm.toString(), "command")}></input>
                <div className="film-number">{currFilm.toString() + "/" + filmInfo.num_films.toString()}</div>
            </div>

            <div className="btn-group">
                <ArrowForwardIosSharpIcon className="button" onClick={() => sendCommand("next", "command")}/>
                <ArrowBackIosSharpIcon className="button" onClick={() => sendCommand("back", "command")}/>
            </div>
        </div>
    )
}

export default SourceTitle; 