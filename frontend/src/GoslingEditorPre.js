import React from 'react';
import { GROUND_VIZ_BACKEND_URL, VIZ_BACKEND_URL } from './Config';

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';


const { validateGoslingSpec, GoslingComponent } = require("gosling.js");
const { debounce } = require('lodash')
const MonacoEditor = require('react-monaco-editor').default;
const { editor, languages } = require('monaco-editor/esm/vs/editor/editor.api');


export const DEFAULT_SPEC = `
{
    "tracks": [
        {
            "layout": "linear",
            "width": 400,
            "height": 180,
            "data": {
                "url": "https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
                "type": "multivec",
                "row": "sample",
                "column": "position",
                "value": "peak",
                "categories": [
                    "sample 1"
                ],
                "binSize": 5
            },
            "mark": "bar",
            "x": {
                "field": "start",
                "type": "genomic",
                "axis": "bottom"
            },
            "xe": {
                "field": "end",
                "type": "genomic"
            },
            "y": {
                "field": "peak",
                "type": "quantitative",
                "axis": "right"
            },
            "size": {
                "value": 5
            }
        }
    ]
}
`


export const stripJsonComments = (data) => {
    console.log(data)
    //data =  JSON.stringify(data)
    let newData = data.replace(/\\"|"(?:\\"|[^"])*"|(\/\/.*|\/\*[\s\S]*?\*\/)/g, (m, g) => g ? "" : m); // remove comments if exist
    return JSON.parse(newData)
}


const prettifySpec = (spec) => {
    let data = JSON.parse(spec);
    return JSON.stringify(data, null, 2);
}


const updateTheme = (isDarkTheme, editor) => {
    editor.defineTheme(
        'gosling', {
        base: 'vs', // vs, vs-dark, or hc-black
        inherit: true,
        // Complete rules: https://github.com/microsoft/vscode/blob/93028e44ea7752bd53e2471051acbe6362e157e9/src/vs/editor/standalone/common/themes.ts#L13
        rules: [
            {background: '#FFFFFF'},
        ],
        colors: {
            'editorGutter.background': '#FFFFFF',
            'editor.background': '#FFFFFF'
        }
    }

    );
}

function TabPanel(props) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography>{children}</Typography>
          </Box>
        )}
      </div>
    );  
}
TabPanel.propTypes = {
children: PropTypes.node,
index: PropTypes.number.isRequired,
value: PropTypes.number.isRequired,
};

function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
}

class GoslingEditorPre extends React.Component {
    constructor(prop) {
        super(prop);
        this.state = {
            image: this.props.image,
            code: prettifySpec(this.props.spec),
            spec: stripJsonComments(this.props.spec),
            log: { state: 'success', message: '' },
            tabValue: 0,
            question: "",
            isDarkTheme: false
        };
        this.onChange = this.onChange.bind(this)
        this.handleTab = this.handleTab.bind(this)
        this.handleQuestion = this.handleQuestion.bind(this)
        this.submitQuestion = this.submitQuestion.bind(this)
        this.reset = this.reset.bind(this)
        this.WAIT = 500
    }
    editorWillMount() {
        updateTheme(this.state.isDarkTheme, editor);
    }
    editorDidMount(editor, monaco) {
        const acceptedList = ['arrangement', 'layout', 'mark', 'width', 'height'];
        acceptedList.forEach(item => {
            var matches = editor.getModel().findMatches(item);
            matches.forEach(match => {
                editor.createDecorationsCollection([
                    {
                        range: match.range,
                        options: {
                            isWholeLine: true,
                            className: "defaultLine"
                        }
                    },
                ]);
            });
        })
    }
    onChange(code, _) {
        try {
            const spec = stripJsonComments(code)
            const validateInfo = validateGoslingSpec(spec)

            if (validateInfo.state = 'success') {

                this.setState({
                    spec,
                    code,
                    log: validateInfo
                })
            } else {
                this.setState({ code, log: validateInfo })
            }
        } catch (e) {
            this.setState({
                code,
                log: { message: '✘ Cannnot parse the code.', state: 'error' }
            })
        }
    }


    reset() {
        this.setState({ spec: stripJsonComments(this.props.spec), code: this.props.spec })
    }

    handleTab(event,newValue){
        console.log(newValue)
        this.setState({tabValue: newValue})
    }

    handleQuestion(e){
        this.setState({question: e.target.value})
    }

    async submitQuestion(){
        const formObject = new FormData();
        formObject.append("predict", "False")
        formObject.append("gostalk_question", this.state.question)
        formObject.append("spec", JSON.stringify(this.state.spec))
        const response = await fetch(VIZ_BACKEND_URL, {
            method: "POST",
            body: formObject
        })
        const json = await response.json()
        const newSpec = JSON.stringify(json["spec"])
        if (newSpec != null){
            this.setState({spec: stripJsonComments(newSpec),
                            code: prettifySpec(newSpec)})
        }

    }

    render() {
        const { log } = this.state
        return (
        <div>
        <div className='gosling-container' id="goslingEditor">
            <div className='grid-item'>
                <p>Original Image</p>
                <img src={this.state.image}/>
                </div>
                <div style={{ margin: '0 0px', overflow: "scroll"}} className='grid-item'>
                <p>Autogosling Results</p>
                    <GoslingComponent
                        spec={this.state.spec}
                        padding={0}
                        className='gosling-component'
                    />
            </div>
        </div>
            <Box sx={{width:'100%'}}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider'}}>
                    <Tabs value={this.state.tabValue} onChange={this.handleTab}>
                        <Tab label="Gos Talk" {...a11yProps(0)}/>
                        <Tab label="Gosling Spec" {...a11yProps(1)}/>
                    </Tabs>
                </Box>
                <TabPanel value={this.state.tabValue} index={0}>
                    <div>
                        <TextField fullWidth 
                            id="outlined-basic" 
                            label="Question" 
                            variant="outlined" 
                            value={this.state.question}
                            onChange={this.handleQuestion}/>
                        <Button onClick={this.submitQuestion}>Submit</Button>
                    </div>
                </TabPanel>
                <TabPanel value={this.state.tabValue} index={1}>
                    <div className='codeContainer' style={{ position: "relative"}}>
                        <MonacoEditor
                            height='70vh'
                            width='100%'
                            language='json'
                            value={this.state.code}
                            onChange={debounce(this.onChange, this.WAIT)}
                            theme="gosling"
                            editorWillMount={this.editorWillMount.bind(this)}
                            editorDidMount={this.editorDidMount}
                            options={{ minimap: { enabled: false }, wordWrap: 'on', scrollBeyondLastLine: false }}
                        />
                        <div className={`compile-message compile-message-${log.state}`}>{log.message}</div>
                        <button type="button" className='float-button' onClick={this.reset}>Reset</button>
                    </div>
                </TabPanel>
            </Box>
        </div>
        )
    }
}

export { GoslingEditorPre };