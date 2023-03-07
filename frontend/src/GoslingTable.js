import React, {useState} from "react"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField";
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import NativeSelect from '@mui/material/NativeSelect';
import MenuItem from '@mui/material/MenuItem';
import OutlinedInput from '@mui/material/OutlinedInput';

import { GROUND_VIZ_BACKEND_URL, VIZ_BACKEND_URL } from './Config';
import { layoutOptions,orientOptions, chartOptions } from "./utils";
import { Select } from "@mui/material";


const properties = ["layout", "mark", "orientation","x", "y", "width", "height", ]
const singleSelectProperties = ["layout", "orientation"]
const multiSelectProperties = ["mark"]
const options = {
    "layout": layoutOptions,
    "orientation":orientOptions,
    "mark":chartOptions
}

const EditableTableCell = ({value,handler,editMode,property}) => {
    const handleChange = (e) => {
        const {
            target:{value},
        } = e;
        handler(value)
    }
    const handleMultipleChange = (e)=>{
        const {
            target:{value},
        } = e;
        handler(typeof value === 'string' ? value.split(','):value,);
    }
    if (!editMode){
        return <TableCell width="10%">
            {value}
            </TableCell>
    } else if (singleSelectProperties.includes(property)){
        return <TableCell width="10%">
            <FormControl fullWidth>
                <InputLabel variant="standard" htmlFor="uncontrolled-native">
                {property}
                </InputLabel>
                <Select
                value={value}
                name="single-select"
                onChange={handleChange}
                input={<OutlinedInput label={property} />}
                inputProps={{
                    name: 'value',
                    id: 'uncontrolled-native',
                }}
                >
                {options[property].map(x=>
                    <MenuItem key={x} value={x}>
                        {x}
                    </MenuItem>)}
                </Select>
            </FormControl>
        </TableCell>
    } else if (multiSelectProperties.includes(property)){
        return <TableCell width="10%">
            <FormControl fullWidth>
                <InputLabel variant="standard" htmlFor="uncontrolled-native">
                {property}
                </InputLabel>
                <Select 
                multiple
                value={value}
                name="multiple-select"
                onChange = {handleMultipleChange}
                input={<OutlinedInput label={property} />}
                >
                    {options[property].map(x=>
                    <MenuItem key={x} value={x}>
                        {x}
                    </MenuItem>)}
                </Select>
            </FormControl>
        </TableCell>
    } else {
        return <TableCell width="10%">
            <TextField variant="outlined" value={value} size="small" onChange={handleChange}/>
        </TableCell>
            
    }
}

const PredictionRow = ({trackInfo,index,createHandler,editMode, selected, handleClick}) => {
    return <TableRow selected = {selected} onClick={e=>handleClick(e,index, selected)}>
        <TableCell width="10%">{index+1}</TableCell>
        {properties.map(property => (
            <EditableTableCell editMode={editMode} handler={createHandler(index,property)} value={trackInfo[property]} property={property} />
        ))}
    </TableRow>

}

export const PredictionTable = ({ currentTracksInfo, setCurrentTracksInfo, selected, setSelected }) => {
    const [editMode, setEditMode] = useState(true)
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

    const handleClick = (e, index, selected) => {
        if (!selected){
            setSelected(oldSelected => {
                const newSelected = oldSelected.map((select,i) => {
                    if (i==index) return !select;
                    else return false;
                })
                return newSelected
            })
            console.log(selected)
        }
    }

    const tableHeadings = properties.map(property => <TableCell>{property}</TableCell>)
    const tableRows = currentTracksInfo.map((trackInfo,index) => 
    <PredictionRow 
        trackInfo={trackInfo} 
        key={index} 
        index={index} 
        createHandler={createChangeHandler} 
        editMode={editMode} 
        selected={selected[index]}
        handleClick={handleClick}/>)
    // alert(JSON.stringify(tracksInfo,null,2))
    return <Table sx={{ minWidth: 650 }} aria-label="gosling bounding box prediction table">
        <TableHead>
            <TableCell>ID</TableCell>
            {tableHeadings}
        </TableHead>
        <TableBody>{tableRows}</TableBody>
        {/* <Button hidden onClick={() => {
            setEditMode(oldValue => !oldValue)
        }}>Toggle edit mode</Button> */}
    </Table >
}