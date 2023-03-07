import React from "react";
import Sketch from "react-p5";

let x = 50;
let y = 50;
let p5Image;


const drawBoxes = (p5,tracksInfo, selected) => {
    for (let i=0; i<tracksInfo.length; i++){
        p5.noFill()
        const {x,y,width, height, layout, mark, orientation} = tracksInfo[i]
        if (selected[i]) p5.stroke(215, 0, 0);
        else p5.stroke(71,102,196);
        p5.strokeWeight(4)
        const rect = p5.rect(x,y,width,height)
        // const message = `Layout: ${layout}\nType: ${mark}\nOrientation: ${orientation}`
        // p5.noStroke()
        // p5.fill(225,245,244)
        p5.rect(x,y,40,30)
        p5.strokeWeight(1)
        if (selected[i]) p5.fill(215, 0, 0);
        else p5.fill(71,102,196);
        // p5.stroke(71,102,196)
        p5.textSize(20)
        p5.text(i+1,x+10,y+20)

    }
}
export default ({image, tracksInfo, width, height, selected, setSelected}) => {
	const setup = (p5, canvasParentRef) => {
		// use parent to render the canvas in this ref
		// (without that p5 will render the canvas outside of your component)
		const cnv = p5.createCanvas(width, height).parent(canvasParentRef);
        cnv.mouseClicked(e=>{
            console.log(e)
            const x = e.offsetX
            const y = e.offsetY
            setSelected(oldSelected => {
                const newSelected = tracksInfo.map((track,index)=> {
                    if (track["x"] <= x && x <= track["x"]+track["width"] &&
                    track["y"] <= y && y <= track["y"]+track["height"]){
                        return !oldSelected[index]
                    } else{
                        return false
                    }
                })
                return newSelected;
            })
        })
        p5.image(p5Image,width,height)
	};
    const preload = (p5) => {
        p5Image = p5.loadImage(image)
    }


	const draw = (p5) => {
        p5.background(0)
        p5.rectMode(p5.CORNER);
        p5.ellipse(width,height,20,20)
        // console.log(p5Image)
        p5.image(p5Image,0,0,width,height)
        drawBoxes(p5,tracksInfo, selected)
		// p5.background(0);
		// p5.ellipse(x, y, 70, 70);
		// NOTE: Do not use setState in the draw function or in functions that are executed
		// in the draw function...
		// please use normal variables or class properties for these purposes
		// x++;
	};

	return <Sketch setup={setup} draw={draw} preload={preload} />;
};