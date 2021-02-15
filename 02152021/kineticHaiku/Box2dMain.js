var physics,
lastFrame = new Date().getTime();

var b2Vec2 = Box2D.Common.Math.b2Vec2;
var b2BodyDef = Box2D.Dynamics.b2BodyDef;
var b2Body = Box2D.Dynamics.b2Body;
var b2FixtureDef = Box2D.Dynamics.b2FixtureDef;
var b2Fixture = Box2D.Dynamics.b2Fixture;
var b2World = Box2D.Dynamics.b2World;
var b2MassData = Box2D.Collision.Shapes.b2MassData;
var b2PolygonShape = Box2D.Collision.Shapes.b2PolygonShape;
var b2CircleShape = Box2D.Collision.Shapes.b2CircleShape;
var b2DebugDraw = Box2D.Dynamics.b2DebugDraw;

window.gameLoop = function() {
    var tm = new Date().getTime();
    requestAnimationFrame(gameLoop);
    var dt = (tm - lastFrame) / 1000;
    if(dt > 1/15) { dt = 1/15; }
    physics.step(dt);
    lastFrame = tm;
};

function init() {
   // var img = new Image();
    
    // Wait for the image to load
    //img.addEventListener("load", function() {
                         
                         physics = window.physics = new Physics(document.getElementById("b2dCanvas"),2);
                        physics.click(function(body) {
                            body.ApplyImpulse({ x: 1000, y: -1000 }, body.GetWorldCenter());
                        });

                         // Create some walls
                         new Body(physics, { color: "red", type: "static", x: 0, y: 0, height: 10,  width: 640 });
                         new Body(physics, { color: "red", type: "static", x: 0, y: 240, height: 10,  width: 640});
                         new Body(physics, { color: "red", type: "static", x: 0, y: 11, height: 480, width: 10 });
                         new Body(physics, { color: "red", type: "static", x: 320, y:11, height: 480, width: 10 });
                         
                       //  new Body(physics, { image: img, x: 5, y: 8 });
                     //    new Body(physics, { image: img, x: 13, y: 8 });
                     //    new Body(physics, { color: "blue", x: 8, y: 3 });
                         new Body(physics, { color: "gray", shape: "circle", radius: 20, x: 110, y: 25 });
                         new Body(physics, { color: "red", shape: "circle", radius: 20, x: 150, y: 25 });
                         new Body(physics, { color: "blue", shape: "circle", radius: 20, x: 190, y: 25 });
    
                         //new Body(physics, { color: "pink", shape: "polygon",
                           //       points: [ { x: 0, y: 0 }, { x: 0, y: 4 },{ x: -10, y: 0 }   ],
                             //     x: 20, y: 5 });
                   

                         requestAnimationFrame(gameLoop);
                        // });
    
   // img.src = "images/bricks.jpg";
}

window.addEventListener("load",init);
//}());

