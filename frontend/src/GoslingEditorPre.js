import React from 'react';

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

const updateTheme = (isDarkTheme, editor) => {
    editor.defineTheme(
        'gosling',
        isDarkTheme
            ? {
                base: 'vs-dark',
                inherit: true,
                rules: [
                    { token: 'string.key.json', foreground: '#eeeeee', fontStyle: 'bold' }, // all keys
                    { token: 'string.value.json', foreground: '#8BE9FD', fontStyle: 'bold' }, // all values
                    { token: 'number', foreground: '#FF79C6', fontStyle: 'bold' },
                    { token: 'keyword.json', foreground: '#FF79C6', fontStyle: 'bold' } // true and false
                ],
                colors: {
                    // ...
                }
            }
            : {
                base: 'vs', // vs, vs-dark, or hc-black
                inherit: true,
                // Complete rules: https://github.com/microsoft/vscode/blob/93028e44ea7752bd53e2471051acbe6362e157e9/src/vs/editor/standalone/common/themes.ts#L13
                rules: [
                    { token: 'string.key.json', foreground: '#222222' }, // all keys
                    { token: 'string.value.json', foreground: '#035CC5' }, // all values
                    { token: 'number', foreground: '#E32A4F' },
                    { token: 'keyword.json', foreground: '#E32A4F' } // true and false
                ],
                colors: {
                    // ...
                }
            }
    );
}

class GoslingEditorPre extends React.Component {
    constructor(prop) {
        super(prop);
        this.state = {
            code: this.props.spec,
            spec: stripJsonComments(this.props.spec),
            log: { state: 'success', message: '' },
            isDarkTheme: false
        };
        this.onChange = this.onChange.bind(this)
        this.reset = this.reset.bind(this)
        this.WAIT = 500
    }
    editorWillMount() {
        updateTheme(this.state.isDarkTheme, editor);
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
    render() {
        const { log } = this.state
        console.log(this.state.spec)
        return <div className='gosling-container' id="goslingEditor">
            <div style={{ margin: '5px 10px' }}>
                <span><b>You can interact with the visualization through zoom and pan, or modify it by changing the code above</b></span>
            </div>
            <div style={{ margin: '0 60px' }}>
                <GoslingComponent
                    spec={this.state.spec}
                    padding={20}
                    className='gosling-component'
                />
            </div>
            <div className='codeContainer' style={{ position: "relative", width: "50%"}}>
                <MonacoEditor
                    height={500}
                    width='100%'
                    language='json'
                    value={this.state.code}
                    onChange={debounce(this.onChange, this.WAIT)}
                    theme="gosling"
                    editorWillMount={this.editorWillMount.bind(this)}
                    options={{ minimap: { enabled: false }, wordWrap: 'on', scrollBeyondLastLine: false }}
                />
                <div className={`compile-message compile-message-${log.state}`}>{log.message}</div>
                <button type="button" className='float-button' onClick={this.reset}>Reset</button>
            </div>
            
        </div>
    }
}

export {GoslingEditorPre};