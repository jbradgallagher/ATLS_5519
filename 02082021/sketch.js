// May the 4th Scrolling Text
// The Coding Train / Daniel Shiffman
// https://thecodingtrain.com/CodingChallenges/101-may-the-4th.html
// https://youtu.be/fUkF-YLLXeg

let font;
let lines;
let myText = [];

let txt = "\n";
let y = 0;
let ysum = 0;

function preload() {
  materials = ["SAND","BRICK","STRAW","DRIFTWOOD","WOOD","SUNLIGHT","WIND","DUST","STARDUST","TURBULENT DREAMS","DREAMS"];
  preps= ["IN", "ON","INSIDE", "OUTSIDE", "UNDERNEATH", "BEHIND"];
  places=["EARTH", "THE GROUND", "HEAVEN", "HELL", "THE OCEAN", "THE DESERT","A ROARING RIVER","A DESOLATE MOON BASE","A DENSE FOREST","A DESERT","A LARGE CITY","A SMALL TOWN"];
  lights=["CANDLELIGHT", "ELECTRIC LIGHT", "A CAMPFIRE", "THE SUN"];
  inhabit=["ALL OF MY FRIENDS", "MY FAMILY", "ALL OF MY ENIMIES", "SOME PRETTY DANGEROUS ANIMALS"];
 
  font = loadFont('AvenirNextLTPro-Demi.otf');
}


function getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min)) + min;
  }

function getRandomWrd(wrdList) {
    return wrdList[getRandomInt(0,wrdList.length-1)];
  }


function setText() {
  txt = txt + "A HOUSE OF " + getRandomWrd(materials) + "\n";
  txt = txt + getRandomWrd(preps) + " " + getRandomWrd(places) + "\n";
  txt = txt + "USING " + getRandomWrd(lights) + "\n";
  txt = txt + "INHABITED BY " + getRandomWrd(inhabit) + "\n";
}

function setup() {
  createCanvas(1280, 720, WEBGL);
  setText()
  y = height / 2;

}

function draw() {
  background(255);
  // No translate(): WEBGL mode starts with the origin in the center.

  fill(0) 
  //fill(238, 213, 75);
  textFont(font);
  textSize(width * 0.04);
  textAlign(LEFT);
  //rotateX(PI / 4);
  let w = width * 0.75;
  text(txt, -w / 2, y, w, height * 10);
  y -= 2;
  if(y < -640) {
    txt = "\n"
    y = height/2
    setText()
  }
  

}
