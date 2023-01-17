import React from "react"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
const properties = ["x", "y", "width", "height", "layout", "mark", "orientation"]
const PredictionRow = (trackInfo) => {
    return <TableRow>
        {properties.map(property => {
            <TableCell>trackInfo[property]</TableCell>
        })}
    </TableRow>

}

/*
export const PredictionTable = ({ tracksInfo }) => {
    const tableHeadings = properties.map(property => <TableCell>{property}</TableCell>)
    const tableRows = tracksInfo.map(trackInfo => <PredictionRow trackInfo={trackInfo} />)
    // alert(JSON.stringify(tracksInfo,null,2))
    return <Table sx={{ minWidth: 650 }} aria-label="gosling bounding box prediction table">
        <TableHead>{tableHeadings}</TableHead>
        <TableBody>{tableRows}</TableBody>
    </Table >
}
*/