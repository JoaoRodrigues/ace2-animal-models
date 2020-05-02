let getTooltip = function(column){
    //column - column component

    //function should return a string for the header tooltip of false to hide the tooltip
    // return column.getDefinition().title;
    return false
}

table = new Tabulator("#models-table", {

	// Data
	ajaxURL: "models/models.json",
	ajaxContentType: "json",
	ajaxResponse: function(url, params, response){
		return response;
	},
	// Formatting
    columns: [
        {title:"Model Name", field:"name", responsive: 0, widthGrow: 2, tooltip: false},
        {title:"Species", field:"species", responsive: 0, widthGrow: 2, tooltip: false},
        {title:"Score", field:"haddock_score", responsive: 0, headerTooltip: getTooltip},
        {title:"vdW", field:"e_vdw", headerTooltip: getTooltip},
        {title:"Electrostatics", field:"e_elec", headerTooltip: getTooltip},
        {title:"Desolvation", field:"e_desolv", headerTooltip: getTooltip},
        {title:"BSA", field:"buried_surf_area", headerTooltip: getTooltip},
    ],
    // Layout
    layout:"fitColumns",
    resizableColumns: false,
    selectable: true,
    columnHeaderVertAlign: "bottom", //align header contents to bottom of cell
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