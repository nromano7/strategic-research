console.log('js loaded.')

function toggleCollapse() {

    var isCollapsed = (
        document.getElementById("collapse-icon").className == "fa fa-plus-circle"
    )

    if (isCollapsed != true) {

        document.getElementById("collapseOne").className = "collapse";
        document.getElementById("collapseTwo").className = "collapse";
        document.getElementById("collapseThree").className = "collapse";
        document.getElementById("collapse-icon").className = "fa fa-plus-circle";

    } else {

        document.getElementById("collapseOne").className = "collapse show";
        document.getElementById("collapseTwo").className = "collapse show";
        document.getElementById("collapseThree").className = "collapse show";
        document.getElementById("collapse-icon").className = "fa fa-minus-circle";

    }
}

// function toggleCollapseButton() {

//     // check if any collapse element is collapsed
//     var oneCollapsed = (
//         document.getElementById("collapseOne").className == "collapse"
//     )
//     var twoCollapsed = (
//         document.getElementById("collapseTwo").className == "collapse"
//     )
//     var threeCollapsed = (
//         document.getElementById("collapseThree").className == "collapse"
//     )

//     if (oneCollapsed || twoCollapsed || threeCollapsed) {
//         // if any collapsed
//         document.getElementById("collapse-icon").className = "fa fa-plus-circle";
//     } else if !(oneCollapsed || twoCollapsed || threeCollapsed) {
//         // if any one open
//         document.getElementById("collapse-icon").className = "fa fa-minus-circle";
//     }


// }

function disableStatus() {
    document.getElementById("status").disabled = true
}

function enableStatus() {
    document.getElementById("status").disabled = false
}

function setSortOption(docType) {
    if (docType == 'project') {
        document.getElementsByName("sortBy")[0].options[2].text = "Start Date"
    } else if (docType == 'publication') {
        document.getElementsByName("sortBy")[0].options[2].text = "Publication Date"
    }
}

function setButtonState(buttonStates) {

    console.log(buttonStates)

    // let topic = "{{ buttonStates['topic']|safe }}"
    // let element = "{{ buttonStates['element']|safe }}"
    // let docType = "{{ buttonStates['doc_type']|safe }}"
    // let status = "{{ buttonStates['status']|safe }}"
    // let dateRange = "{{ buttonStates['date_range']|safe }}"
    // let sortBy = "{{ buttonStates['sort_by']|safe }}"
    // let rpp = "{{ buttonStates['rpp']|safe }}"

    let topic = buttonStates.topic
    let element = buttonStates.element
    let docType = buttonStates.doc_type
    let status = buttonStates.status
    let dateRange = buttonStates.date_range
    let sortBy = buttonStates.sort_by
    let rpp = buttonStates.rpp

    // update 'topic' selection
    if (topic == 'all') {
        document.getElementsByName('topic')[0].options.selectedIndex = 1
    } else if (topic == 'construction_quality') {
        document.getElementsByName('topic')[0].options.selectedIndex = 2
    } else if (topic == 'design_and_details') {
        document.getElementsByName('topic')[0].options.selectedIndex = 3
    } else if (topic == 'material_specifications') {
        document.getElementsByName('topic')[0].options.selectedIndex = 4
    } else if (topic == 'live_load') {
        document.getElementsByName('topic')[0].options.selectedIndex = 5
    } else if (topic == 'maintenance_and_preservation') {
        document.getElementsByName('topic')[0].options.selectedIndex = 6
    } else if (topic == 'structural_integrity') {
        document.getElementsByName('topic')[0].options.selectedIndex = 7
    } else if (topic == 'structural_condition') {
        document.getElementsByName('topic')[0].options.selectedIndex = 8
    } else if (topic == 'functionality') {
        document.getElementsByName('topic')[0].options.selectedIndex = 9
    } else if (topic == 'cost') {
        document.getElementsByName('topic')[0].options.selectedIndex = 10
    }


    // update 'element' selection
    if (element == 'all') {
        document.getElementsByName('element')[0].options.selectedIndex = 1
    } else if (element == 'superstructure') {
        document.getElementsByName('element')[0].options.selectedIndex = 2
    } else if (element == 'untreated_deck') {
        document.getElementsByName('element')[0].options.selectedIndex = 3
    } else if (element == 'treated_deck') {
        document.getElementsByName('element')[0].options.selectedIndex = 4
    } else if (element == 'joints') {
        document.getElementsByName('element')[0].options.selectedIndex = 5
    } else if (element == 'bearings') {
        document.getElementsByName('element')[0].options.selectedIndex = 6
    } else if (element == 'coatings') {
        document.getElementsByName('element')[0].options.selectedIndex = 7
    } else if (element == 'prestressing') {
        document.getElementsByName('element')[0].options.selectedIndex = 8
    }

    //  update record type selection
    console.log(docType)
    if (docType == 'project') {
        document.getElementById('rt2').checked = true
        setSortOption(docType)
        enableStatus()
    } else {
        document.getElementById('rt3').checked = true
        setSortOption(docType)
        disableStatus()
    }

    // update status selection
    if (status == 'all') {
        document.getElementsByName('status')[0].options.selectedIndex = 1
    } else if (status == 'active') {
        document.getElementsByName('status')[0].options.selectedIndex = 2
    } else if (status == 'complete') {
        document.getElementsByName('status')[0].options.selectedIndex = 3
    } else if (status == 'programmed') {
        document.getElementsByName('status')[0].options.selectedIndex = 4
    } else if (status == 'proposed') {
        document.getElementsByName('status')[0].options.selectedIndex = 5
    }

    // update date range selection
    if (dateRange == '1') {
        document.getElementById('dr1').checked = true
    } else if (dateRange == '5') {
        document.getElementById('dr2').checked = true
    } else if (dateRange == '50') {
        document.getElementById('dr3').checked = true
    }

    // update rpp selection
    if (rpp == '5') {
        document.getElementById('rpp1').checked = true
    } else if (rpp == '10') {
        document.getElementById('rpp2').checked = true
    }

    // update sort selection
    if (sortBy == 'score') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 1
    } else if (sortBy == 'date') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 2
    } else if (sortBy == 'both') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 3
    }

}

let page = "{{ page|safe }}"
if (page == '1') {
    document.getElementById("leftArrow1").className = "page-item disabled mr-1"
    document.getElementById("leftArrow2").className = "page-item disabled mr-1"
    document.getElementById("leftArrow3").className = "page-item disabled mr-1"
}