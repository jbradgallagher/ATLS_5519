var Body = window.Body = function (physics, aContext, details) {
    this.details = details;
    this.physics = physics;

    //var actxCall = window.webkitAudioContext || window.AudioContext;
   //this.audioContext = 
    if(aContext != null) {
        this.aSineWave = new SineWave(aContext);
        //this.aSineWave2 = new SineWave(aContext);
    }
    // Create the definition
    this.definition = new b2BodyDef();
    
    // Set up the definition
    for (var k in this.definitionDefaults) {
        this.definition[k] = details[k] || this.definitionDefaults[k];
    }
    this.definition.position = new b2Vec2(details.x || 0, details.y || 0);
    this.definition.linearVelocity = new b2Vec2(details.vx || 0, details.vy || 0);
    this.definition.userData = this;
    this.definition.type = details.type == "static" ? b2Body.b2_staticBody : b2Body.b2_dynamicBody;
    
    // Create the Body
    this.body = physics.world.CreateBody(this.definition);
    
    // Create the fixture
    this.fixtureDef = new b2FixtureDef();
    for (var l in this.fixtureDefaults) {
        this.fixtureDef[l] = details[l] || this.fixtureDefaults[l];
    }
    
    
    details.shape = details.shape || this.defaults.shape;
    
    switch (details.shape) {
        case "circle":
            details.radius = details.radius || this.defaults.radius;
            this.fixtureDef.shape = new b2CircleShape(details.radius);
            break;
        case "polygon":
            this.fixtureDef.shape = new b2PolygonShape();
            this.fixtureDef.shape.SetAsArray(details.points, details.points.length);
            break;
        case "block":
        default:
            details.width = details.width || this.defaults.width;
            details.height = details.height || this.defaults.height;
            
            this.fixtureDef.shape = new b2PolygonShape();
            this.fixtureDef.shape.SetAsBox(details.width / 2,
                                           details.height / 2);
            break;
    }
    
    this.body.CreateFixture(this.fixtureDef);
    
    this.playing = false;
    this.amplitude = 0.1;

};


Body.prototype.defaults = {
shape: "block",
width: 5,
height: 5,
radius: 2.5
};

Body.prototype.fixtureDefaults = {
density: 2,
friction: 1,
restitution: 0.2
};

Body.prototype.definitionDefaults = {
active: true,
allowSleep: true,
angle: 0,
angularVelocity: 0,
awake: true,
bullet: false,
fixedRotation: false
};

Body.prototype.draw = function (context,text,numSyl) {
    var tidx = 0;
    var pos = this.body.GetPosition(),
    angle = this.body.GetAngle();
    var vel = this.body.GetLinearVelocity();
    var angVel = this.body.GetAngularVelocity();
    //if(angVel != 0.0)
    //   this.aSineWave.setFmFrequency(Math.abs(angVel)*0.5);
    // Save the context
    context.save();
    
    // Translate and rotate
    context.translate(pos.x, pos.y);
    context.rotate(angle);
    
    // Draw the shape outline if the shape has a color
    if (this.details.color) {
        if(this.details.impulseActive) {
            context.fillStyle = this.details.colorTwo;
        } else {
            context.fillStyle = this.details.color;
        }
        
        switch (this.details.shape) {
            case "circle":
                context.beginPath();
                context.arc(0, 0, this.details.radius, 0, Math.PI * 2);
                context.fill();
                context.strokeStyle = "black";
                context.stroke();
                var font = "bold " + this.details.radius +"px serif";
                context.font = font;
                context.textBaseline = "top";
                context.lineWidth = 3;
                context.strokeText(text, 20-(this.details.radius)/4 ,20-(this.details.radius)/2);
                context.fillText(text, 20-(this.details.radius)/4 ,20-(this.details.radius)/2);
                context.fillStyle = "black";
                context.fillText(numSyl, -this.details.radius/4, -this.details.radius/4);
                context.closePath();
                break;
            case "polygon":
                var points = this.details.points;
                context.beginPath();
                context.moveTo(points[0].x, points[0].y);
                for (var i = 1; i < points.length; i++) {
                    context.lineTo(points[i].x, points[i].y);
                }
                context.fill();
                context.closePath();
                break;
            case "block":
                context.beginPath();
                context.fillRect(-this.details.width / 2, -this.details.height / 2,
                                 this.details.width,
                                 this.details.height);
                context.closePath();
                break;
            default:
                break;
        }
    }
    
    // If an image property is set, draw the image.
    if (this.details.image) {
        context.drawImage(this.details.image, -this.details.width / 2, -this.details.height / 2,
                          this.details.width,
                          this.details.height);
        
    }
    
    context.restore();
};

Body.prototype.drawTwo = function (context,text) {
    var tidx = 0;
    var pos = this.body.GetPosition(),
    angle = this.body.GetAngle();
    var vel = this.body.GetLinearVelocity();
    
    // Save the context
    context.save();
    
    // Translate and rotate
    context.translate(pos.x, pos.y);
    context.rotate(angle);
    
    
    // Draw the shape outline if the shape has a color
    if (this.details.color) {
        if(this.details.impulseActive) {
            context.fillStyle = this.details.colorTwo;
        } else {
            context.fillStyle = this.details.color;
        }
        
        switch (this.details.shape) {
            case "circle":
                var font = "bold " + this.details.radius +"px courier";
                context.font = font;
                context.textBaseline = "top";
                context.strokeStyle = "black";
                context.lineWidth = 1;
                context.strokeText(text, 20-(this.details.radius)/4 ,20-(this.details.radius)/2);
                context.fillText(text, 20-(this.details.radius)/4 ,20-(this.details.radius)/2);
                
                break;
            case "polygon":
                break;
            case "block":
                break;
            default:
                break;
        }
    }
    
    context.restore();
};

Body.prototype.setTextColor = function (context,vel) {
    if(this.details.impulseActive) {
        if(vel < 0.0) {
            context.fillStyle = "#ad0000";
        } else {
            context.fillStyle = "#0b0751";
        }
            
    } else {
        if(this.details.color == "#4370ba")
            context.fillStyle = "#ffee05";
        if(this.details.color == "#ff8a05")
            context.fillStyle = "black";
        if(this.details.color == "#58ba43")
            context.fillStyle = "#a02216";
    }
}

Body.prototype.PlayTone = function(caller,midiNote) {
    if(!this.playing) {
        this.playing = true;
        this.player = caller;
        //this.aSineWave = new SineWave(physics.audioContext);
        // this.setToneByYLocation();
        //console.log("PT: ",this.physics.halfSteps.length,this.physics.halfStepsTwo.length);
        this.aSineWave.setFrequency(this.GetFreq(midiNote));
        //this.physics.makeNewHalfSteps(idx);
        //this.physics.makeNewHalfStepsTwo(idx);
        
        if(this.details.badTone) {
            this.aSineWave.setFmFrequency(Math.abs(this.body.GetAngularVelocity()));
            //this.details.badTone = false;
        }
        this.aSineWave.setAmplitude(this.amplitude);
        //   for (var i = 0; i < this.connections.length; i++) {
        //     this.aSineWave.getOutNode().connect(this.connections[i]);
        //}
        this.aSineWave.play();
    }
}

Body.prototype.PauseTone = function (caller) {
    if(this.playing) {
        if(this.player == caller) {
            this.playing = false;
            this.aSineWave.pause();
            //this.aSineWave2.pause();
            this.aSineWave.setFmFrequency(0);
            //this.aSineWave2.setFmFrequency(0);
        }
    }
}

Body.prototype.getRandomInt = function(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}



Body.prototype.GetFreq = function(midiNote) {
    //var halfSteps = [0,2,4,7,9];
    //var halfStepsTwo = [1,3,6,11,15];
    //var halfStepsTwo = [0,2,3,6,8,11];
    var freq = 0.0;
    freq = Math.pow(2, (midiNote-69)/12) * 440.0;
    //console.log("FREq: ",midiNote,freq);
    //if(!badTone) {
    /*    console.log("TMYK: ",this.physics.halfSteps[idx],this.physics.halfStepsTwo[idx]);
        if(!low) {
            freq = this.details.tone * Math.pow(1.059463094359,this.physics.halfSteps[idx]);
        } else {
            freq = this.details.tone * Math.pow(1.059463094359,this.physics.halfStepsTwo[idx]);
        }*/
   /* } else {
        idx = this.getRandomInt(0,this.physics.halfStepsTwo.length-1);
        freq = 620.0 * Math.pow(1.059463094359,this.physics.halfStepsTwo[idx]);
        this.physics.makeNewHalfStepsTwo(idx);
    }*/
   /* if(this.details.wordType == "noun" || this.details.wordType == "verb") {
        if(Math.random() > 0.5) {
            freq = this.details.tone * Math.pow(1.059463094359,halfSteps[Math.floor(Math.random()*halfSteps.length)]);
        } else {
            freq = this.details.tone / Math.pow(1.059463094359,halfStepsTwo[Math.floor(Math.random()*halfSteps.length)]);
        }
    }
        if(this.details.wordType == "adj" || this.details.wordType == "adv") {
            if(Math.random() > 0.5) {
                freq = this.details.tone * Math.pow(1.059463094359,halfStepsTwo[Math.floor(Math.random()*halfStepsTwo.length)]);
            } else {
                freq = this.details.tone / Math.pow(1.059463094359,halfStepsTwo[Math.floor(Math.random()*halfStepsTwo.length)]);
            }
        }*/
    return freq;
}
