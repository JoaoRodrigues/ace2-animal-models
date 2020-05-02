table = new Tabulator("#models-table", {
	
	// Data
	ajaxURL: "models/models.json",
	ajaxContentType: "json",
	ajaxResponse: function(url, params, response){
		return response;
	},
	// Formatting
    columns: [
        {title:"Model Name", field:"name", responsive: 0, widthGrow: 2},
        {title:"Species", field:"species", responsive: 0, widthGrow: 2},
        {title:"Score", field:"haddock_score", responsive: 0},
        {title:"vdW", field:"e_vdw"},
        {title:"Electrostatics", field:"e_elec"},
        {title:"Desolvation", field:"e_desolv"},
        {title:"BSA", field:"buried_surf_area"},
    ],
    // Layout
    layout:"fitColumns",
    resizableColumns: false,
	// groupBy:"species",
    selectable: true,
    columnHeaderVertAlign:"bottom", //align header contents to bottom of cell
	responsiveLayout: "hide", // hide rows that no longer fit
    pagination: "local",
    paginationSize: 5,  // model per page.

    // Callbacks
 	rowSelected:function(row){
 		let pdburl = "models/" + row.getData().url;
 		let pdbname = row.getData().name;
 		loadMolecule(stage, pdburl)
 	},

 	rowDeselected:function(row){
 		let pdburl = "models/" + row.getData().url;
 		let pdbname = row.getData().name;
 		removeMolecule(stage, pdburl)
 	},

});