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


const properties = ["x", "y", "width", "height", "layout", "mark", "orientation"]
const singleSelectProperties = ["layout", "orientation"]
const multiSelectProperties = ["mark"]
const options = {
    "layout": layoutOptions,
    "orientation":orientOptions,
    "mark":chartOptions
}

const EditableTableCell = ({value,handler,editMode,property}) => {
    const handleChange = (e) => {
        const newValue = e.target.value
        handler(newValue)
    }
    const handleMultipleChange = (e)=>{
        const {
            target:{value},
        } = e;
        handler(typeof value === 'string' ? value.split(','):value,);
    }
    if (!editMode){
        return <TableCell>
            {value}
            </TableCell>
    } else if (singleSelectProperties.includes(property)){
        return <TableCell>
            <FormControl fullWidth>
                <InputLabel variant="standard" htmlFor="uncontrolled-native">
                {property}
                </InputLabel>
                <NativeSelect
                defaultValue={value}
                onChange={handleChange}
                inputProps={{
                    name: 'value',
                    id: 'uncontrolled-native',
                }}
                >
                {options[property].map(x=><option value={x}>{x}</option>)}
                </NativeSelect>
            </FormControl>
        </TableCell>
    } else if (multiSelectProperties.includes(property)){
        return <TableCell>
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
        return <TableCell>
            <TextField variant="outlined" value={value} size="small" onChange={handleChange}/>
        </TableCell>
            
    }
}

const PredictionRow = ({trackInfo,index,createHandler,editMode}) => {
    return <TableRow>
        {properties.map(property => (
            <EditableTableCell editMode={editMode} handler={createHandler(index,property)} value={trackInfo[property]} property={property} />
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
        <Button onClick={() => {
            setEditMode(oldValue => !oldValue)
        }}>Toggle edit mode</Button>
    </Table >
}