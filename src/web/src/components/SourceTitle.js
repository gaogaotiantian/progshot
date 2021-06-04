import '../App.css';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import KeyboardArrowLeftIcon from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@material-ui/icons/KeyboardArrowRight';
import SubdirectoryArrowLeftIcon from '@material-ui/icons/SubdirectoryArrowLeft';
import SubdirectoryArrowRightIcon from '@material-ui/icons/SubdirectoryArrowRight';


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
                <SubdirectoryArrowRightIcon className="button" title="return" style={{fontSize: 30}} onClick={() => sendCommand("return", "command")}/>
                <KeyboardArrowDownIcon className="button" fontSize="large" onClick={() => sendCommand("next", "command")}/>
                <KeyboardArrowRightIcon className="button" fontSize="large" onClick={() => sendCommand("step", "command")}/>
                <SubdirectoryArrowLeftIcon className="button" style={{fontSize: 30}} onClick={() => sendCommand("rb", "command")}/>
                <KeyboardArrowUpIcon className="button" fontSize="large" onClick={() => sendCommand("back", "command")}/>
                <KeyboardArrowLeftIcon className="button" fontSize="large" onClick={() => sendCommand("stepback", "command")}/>
            </div>
        </div>
    )
}

export default SourceTitle; 
