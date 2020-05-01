// NGL
document.addEventListener("DOMContentLoaded", function () {

  let stageParams = { backgroundColor: "white", tooltip: true};
  stage = new NGL.Stage("viewer", stageParams);

  // create tooltip element and add to the viewer canvas
  let tooltip = document.createElement("div");
  tooltip.setAttribute("id", "ngl-tooltip");
  Object.assign(tooltip.style, {
    display: "none",
    position: "absolute",
    zIndex: 10,
    pointerEvents: "none",
    backgroundColor: "rgba(0, 0, 0, 0.6)",
    color: "lightgrey",
    padding: "0.4em",
    fontFamily: "sans-serif"
  });
  stage.viewer.container.appendChild(tooltip);

  // Handle resizing events
  function handleResize() {
    stage.handleResize();
  }

  window.addEventListener("resize", handleResize, false);

  loadMolecule(stage, reference);

});

let schemeId = NGL.ColormakerRegistry.addScheme( function( params ){
    this.atomColor = function( atom ){
        if (atom.element == 'N'){
          return 0x427DA5;
        }
        else if (atom.element == 'O'){
          return 0x9D272D;
        }
        else if (atom.element == 'H'){
          return 0xf2f2f2;
        }
        else if (atom.element == 'S'){
          return 0xffb347;
        }
        else if (atom.element == 'C' && atom.chainname == 'B'){
          return 0xEBF5FB;
        }
        else if (atom.element == 'C' && atom.chainname == 'E'){
          return 0xC5F1C5;
        }
        else {
            return 0xFFFFFF;
        }
    };
} );

// let schemeId = NGL.ColormakerRegistry.addSelectionScheme([
//   ["red", "_O"],
//   ["blue", "_N"],
//   ["gold", "_S"],
//   ["lightgray", '_C'],
//   ["white", "*"]
// ], "lightscheme");

function selectInterface(c) {
  // Because NGL is incredibly clutsy, we have to do this..

  let radius = 5.0;
  let selection = '';
  let neighborsE;
  let neighborsB;

  // neighbors of E belonging to B
  nglsele = new NGL.Selection(":E");
  neighborsE = c.structure.getAtomSetWithinSelection(nglsele, radius);
  neighborsE = c.structure.getAtomSetWithinGroup(neighborsE);
  selection += "((" + neighborsE.toSeleString() + ") and :B)"

  nglsele = new NGL.Selection(":B");
  neighborsB = c.structure.getAtomSetWithinSelection(nglsele, radius);
  neighborsB = c.structure.getAtomSetWithinGroup(neighborsB);
  selection += "or ((" + neighborsB.toSeleString() + ") and :E)"

  return selection

}

// Load molecule function
function loadMolecule(stage, model) {

    let components = stage.compList;

    component = stage.loadFile(
      model,
      { ext: "pdb" }
    ).then( function (c) {

      c.addRepresentation(
        'cartoon',
        {
          sele: 'protein', 
          color: schemeId,
          aspectRatio: 5.0,
          // quality: 'high' 
        }
      );

      c.addRepresentation(
        'hyperball',
        {
          sele: selectInterface(c),
          color: schemeId
        }
      );

      if (components.length > 1) {
        // Superpose on previous

        c.superpose(
          components[0],
          true,
          ".CA",
          ".CA"
        );
      } else {
        // Adjust view to loaded molecule
        // Do it on first only, since all others are aligned
        let pa = c.structure.getView(new NGL.Selection(".CA or .C5'")).getPrincipalAxes();
        stage.animationControls.rotate(pa.getRotationQuaternion(), 0);
        stage.autoView();
      }

    });

}

function removeMolecule(stage, pdburl) {

    let components = stage.compList;
    for (let i = 0; i < components.length; i++){
      s = components[i].structure;
      if (s.path == pdburl) {
        stage.removeComponent(components[i])
      }
    }

}

function toggleReference() {
  let label = document.getElementById('refe-toggler')
  if (label.innerText.trim() == "Show Reference") 
  {
    label.innerText = "Hide Reference";
    loadMolecule(stage, reference);
  }
  else {
    label.innerText = "Show Reference";
    removeMolecule(stage, reference);
  }
}

function toggleContacts() {

  let components = stage.compList;

  let label = document.getElementById('cont-toggler')
  if (label.innerText.trim() == "Show Contacts") 
  {
    label.innerText = "Hide Contacts";

    for (let i = 0; i < components.length; i++){
      c = components[i];
      // Show interface as hyperballs
      c.addRepresentation(
        'contact',
        {
          sele: selectInterface(c)
        }
      );
    }
  }
  else {
    label.innerText = "Show Contacts";

    for (let i = 0; i < components.length; i++){
      c = components[i];
      let repr = null;
      for(let j = 0; j < c.reprList.length; j++) {
        let r = c.reprList[j];
        if (r.name == 'contact') {
          repr = r;
        }
      }
      if (repr) {
        c.removeRepresentation(repr)
      }
    }
  }
}