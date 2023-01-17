import React, {useState} from "react"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
// import EditIcon from '@mui/icons-material/Edit';
const properties = ["x", "y", "width", "height", "layout", "mark", "orientation"]


const EditableTableCell = ({value,handler,editMode}) => {
    if (!editMode){
        return <TableCell>
            {value}
            </TableCell>
    } else {
        const handleChange = (e) => {
            const newValue = e.target.value
            handler(newValue)
        }
        return <TableCell>
            <TextField variant="outlined" value={value} size="small" onChange={handleChange}/>
        </TableCell>
            
    }
}

const PredictionRow = ({trackInfo,index,createHandler,editMode}) => {
    return <TableRow>
        {properties.map(property => (
            <EditableTableCell editMode={editMode} handler={createHandler(index,property)} value={trackInfo[property]}/>
        ))}
    </TableRow>

}

export const PredictionTable = ({ currentTracksInfo, setCurrentTracksInfo }) => {
    const [editMode, setEditMode] = useState(false)
    const createChangeHandler = (index, property) => (newValue) => {
        setCurrentTracksInfo(oldTracksInfo => {
            const newTracksInfo = oldTracksInfo.map((trackInfo,currentIndex) =>{
                if (currentIndex !== index){
                    return trackInfo
                }
                const modifiedTrackInfo = Object.assign({},trackInfo,{[property]: newValue})
                return modifiedTrackInfo
            })
            // debugger
            return newTracksInfo
        })
    }
    const tableHeadings = properties.map(property => <TableCell>{property}</TableCell>)
    const tableRows = currentTracksInfo.map((trackInfo,index) => <PredictionRow trackInfo={trackInfo} key={index} index={index} createHandler={createChangeHandler} editMode={editMode}/>)
    // alert(JSON.stringify(tracksInfo,null,2))
    return <Table sx={{ minWidth: 650 }} aria-label="gosling bounding box prediction table">
        <TableHead>{tableHeadings}</TableHead>
        <TableBody>{tableRows}</TableBody>
        <Button onClick={() => setEditMode(oldValue => !oldValue)}>Toggle edit mode</Button>
    </Table >
}