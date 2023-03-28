import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import { GROUND_VIZ_BACKEND_URL, VIZ_BACKEND_URL } from './Config';
import './App.css';
import { GoslingEditorPre, DEFAULT_SPEC,stripJsonComments } from './GoslingEditorPre';
import {GoslingComponent} from "gosling.js";
import GoslingSketch from "./GoslingSketch"
import { EX_SPEC_BASIC_SEMANTIC_ZOOM } from "./default_specs";
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import TextField from '@mui/material/TextField';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { PredictionTable } from './GoslingTable';

const UploadImageComponent = ({ handleFile } : {handleFile : any}) => (
  <Box className="setup">
    <Box className="uploadBox" sx={{ width: '100%' }}>
      <form>
        <Button variant="contained" component="label">Choose image to analyze
          <input type="file" name="image" id="image" hidden onChange={handleFile} />
        </Button>
      </form>
    </Box>
  </Box>
)
function AppStepper({ data, step, handleFile, showData }: { data: any, handleFile : any, step: any, showData : any }) {
  debugger 
  const initialTracksInfo = !!data ? data.tracks_info : []
  const initialSpec = !!data ? data.spec : []
  console.log(initialSpec)
  const [spec,setSpec] = useState(() => initialSpec)
  console.log(spec)
  const [currentTracksInfo, setCurrentTracksInfo] = useState(()=>initialTracksInfo)
  const initialSelected = new Array(currentTracksInfo.length).fill(false)
  const [selected, setSelected] = useState(() => initialSelected)
  console.log(selected)
  const [expanded, setExpanded] = useState(true);
  const [gostalkQuestion, setGostalkQuestion] = useState("")

  //const [confirmed, setConfirmed] = useState(false);
  useEffect(() => {
    setCurrentTracksInfo(initialTracksInfo)
    setSpec(initialSpec)
    setSelected(() => initialSelected)
  },[data])
  if (!showData){
    return <UploadImageComponent handleFile={handleFile}/>
  }
  if (JSON.stringify(data) === "{}"){
    return <div>AutoGosling could not find the ground truth in the dataset</div>
  }
  const { tracks_info: tracksInfo, image, width, height} = data
  
  const submitTable = async () =>{
    console.log("Submit table")
    const formObject = new FormData();
    formObject.append("predict", "False")
    formObject.append("track_info", JSON.stringify(currentTracksInfo))
    const response = await fetch(VIZ_BACKEND_URL, {
        method: "POST",
        body: formObject
      })
    const json = await response.json()
    if (json["spec"] != null){
      setSpec(json["spec"])
    }
    setSelected(() => initialSelected)
  }

  const addTrack = async () =>{
    const formObject = new FormData();
    formObject.append("predict", "False")
    formObject.append("append", "True")
    formObject.append("track_info", JSON.stringify(currentTracksInfo))
    const response = await fetch(VIZ_BACKEND_URL, {
        method: "POST",
        body: formObject
      })
    const json = await response.json()
    if (json["spec"] != null){
      setSpec(json["spec"])
    }
    if (json["tracks_info"] != null){
      setCurrentTracksInfo(json["tracks_info"])
      console.log(currentTracksInfo)

    }
  }

  const deleteSelectedTrack = async () =>{
    const formObject = new FormData();
    formObject.append("predict", "False")
    formObject.append("delete", "True")
    formObject.append("track_info", JSON.stringify(currentTracksInfo))
    formObject.append("selected", JSON.stringify(selected))
    const response = await fetch(VIZ_BACKEND_URL, {
        method: "POST",
        body: formObject
      })
    const json = await response.json()
    if (json["spec"] != null){
      setSpec(json["spec"])
    }
    if (json["tracks_info"] != null){
      setCurrentTracksInfo(json["tracks_info"])
      console.log(currentTracksInfo)

    }
  }

  const reset = () =>{
    setSpec(() => initialSpec)
    setCurrentTracksInfo(() => initialTracksInfo)
  }

  const handleExpanded = () => {
    setExpanded(prev => !prev)
  }
  const handleQuestionChange = (event: React.ChangeEvent<HTMLInputElement>) =>{
    setGostalkQuestion(event.target.value)
  }

  const submitQuestion = async () => {
    const formObject = new FormData();
    formObject.append("predict", "False")
    formObject.append("gostalk_question", gostalkQuestion)
    formObject.append("spec", JSON.stringify(spec))
    const response = await fetch(VIZ_BACKEND_URL, {
      method: "POST",
      body: formObject
    })
    const json = await response.json()
    if (json["spec"] != null){
      setSpec(json["spec"])
    }
    if (json["tracks_info"] != null){
      setCurrentTracksInfo(json["tracks_info"])
      console.log(currentTracksInfo)
    }
  }

  const predictionComponent = (<div>
    <div className='gosling-container' id="goslingEditor">
    <div className='grid-item'>
      <p>Original Image</p>
      <GoslingSketch 
        image={image} 
        tracksInfo={currentTracksInfo} 
        width={width} 
        height={height} 
        selected={selected} 
        setSelected={setSelected} />
    </div>
    <div style={{ margin: '0 0px', overflow: "scroll"}} className='grid-item'>
    <p>Autogosling Results</p>
        <GoslingComponent
            spec={spec}
            padding={0}
            className='gosling-component'
        />
    </div>
    </div>
    <PredictionTable currentTracksInfo={currentTracksInfo} setCurrentTracksInfo={setCurrentTracksInfo} selected={selected} setSelected={setSelected}></PredictionTable>
    <Button onClick={()=> addTrack()}> Add A New Track</Button>
    <Button onClick={()=> deleteSelectedTrack()}> Delete Selected Track</Button>
    <Button onClick={()=> reset()}> Reset</Button>
    <Button onClick={() => submitTable()}>Confirm</Button>
    {/* {confirmed && <p>Changes have been saved!</p> } -->*/}
  </div>)
  const editorComponent = !!data.spec ? <div>
    <div>
      <Accordion expanded={expanded} onChange={handleExpanded}>
        <AccordionSummary
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Original Image</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <img src={image} />
        </AccordionDetails>
      </Accordion>
    
    </div>
    <GoslingEditorPre spec={JSON.stringify(spec)} />
  </div> : <div>AutoGosling could not generate a spec file as there was nothing detected.</div>;
  // alert('hi')

  const gostalkComponent = (
    <div>
    <div className='gosling-container'>
    <div className='grid-item'>
      <p>Original Image</p>
      <GoslingSketch 
        image={image} 
        tracksInfo={currentTracksInfo} 
        width={width} 
        height={height} 
        selected={selected} 
        setSelected={setSelected} />
    </div>
    <div style={{ margin: '0 0px', overflow: "scroll"}} className='grid-item'>
    <p>Autogosling Results</p>
        <GoslingComponent
            spec={spec}
            padding={0}
            className='gosling-component'
        />
    </div>
    </div>
    <div>
      <TextField fullWidth 
      id="outlined-basic" 
      label="Question" 
      variant="outlined" 
      value={gostalkQuestion}
      onChange={handleQuestionChange}/> </div>
    <div>
    <Button onClick={()=>submitQuestion()}>Submit</Button>
    </div>
    </div>
  )
  const componentArray = [<UploadImageComponent handleFile={handleFile}/>, predictionComponent, editorComponent, gostalkComponent]
  return componentArray[step]

}

function App() {
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState()
  const [error, setError] = useState(false)
  const [useGround, setUseGround] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  const handleFile = async (e: any) => {
    const formObject = new FormData(e.target.form)
    formObject.append("predict", "True")
    console.log(formObject)
    const response = await fetch(useGround ? GROUND_VIZ_BACKEND_URL : VIZ_BACKEND_URL, {
      method: "POST",
      body: formObject
    })
    const json = await response.json()
    setData(json)
    setError(!response.ok)
    setHasData(true)
    setActiveStep(prev => prev + 1)
  }

  const handleNavigation = () => {
    setActiveStep((prevActiveStep) => Math.min(2,prevActiveStep+1));
  }
  const MAX_STEPS = 3
  return (
    <div className="App">
      <Typography>
        <h1 className="page-title">AutoGosling</h1>
        {/* <Button variant="outlined" onClick={() => setUseGround(prev => !prev)}>{useGround ? "Currently showing Ground Truth. Click to show predictions" : "Currently showing predictions. Click to show ground truth"}</Button> */}
      </Typography>
      <Box className="results" sx={{ width: '100%' }}>
        <Box sx={{ width: '100%' }}>
          <Stepper activeStep={activeStep}>
            <Step key={0} completed={false}>
              <Typography>
                <StepLabel>Upload</StepLabel>
              </Typography>
            </Step>
            <Step key={1} completed={false}>
              <Typography>
                <StepLabel>Detection</StepLabel>
              </Typography>
            </Step>
            <Step key={2} completed={false}>
              <Typography>
                <StepLabel>Customization</StepLabel>
              </Typography>
            </Step>
            <Step key={3} completed={false}>
              <Typography>
                <StepLabel>GosTalk</StepLabel>
              </Typography>
            </Step>
          </Stepper>

        </Box>
        <Box className="stepper-buttons">
          <Box style={{ flex: "1 1 auto" }} hidden={activeStep === 2}></Box>
          {activeStep != 0 &&
          <Button variant="contained" onClick={() => setActiveStep(prev => Math.max(prev -1,0))}>
            Back
          </Button>
          }
          {activeStep != MAX_STEPS && <Button variant="contained" onClick={() => { 
            setActiveStep(prev => Math.min(prev + 1,10))
          }}>
            Next
          </Button>}
        </Box>
        <AppStepper showData={hasData && !error} data={data} step={activeStep} handleFile={handleFile}/>
      </Box>
    </div >
  );
}

export default App;