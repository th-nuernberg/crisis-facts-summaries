// Initial Assignement for Button analyse
function initAssignment(){

    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)

    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = document.getElementById("field_more_opt");
            if (content.style.maxHeight){
            content.style.maxHeight = null;
            } else {
            content.style.maxHeight = content.scrollHeight + "px";
            } 
        });}
}


//Create Options for Dataset dropdown menu
async function getDataset(){
let response_json;

    await fetch("http://127.0.0.1:5000/datasets", 
        {
            method: 'GET',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
        }).then( (response) =>{    
                //It returns a promise which resolves with the result of parsing the body text as JSON
                return response.json();
        }).then(jsonResponse=>{
            response_json = jsonResponse
        }).catch((err) => console.error(err));

        let data_dropdown = document.getElementById("type_of_dataset");
        
        for(let i = 0; i < response_json["files"].length; i++){
            let new_option = document.createElement("option");
            new_option.setAttribute('class',"dropbtn_opt");
            new_option.setAttribute('value',response_json["files"][i]);
            new_option.innerHTML=response_json["files"][i];
            data_dropdown.appendChild(new_option);
        }    
}


async function make_a_summary(){
    //if there is already a summary, remove it 
    if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
    }

    //Get all Parameters
    let variables_for_summary = get_parameter_as_json();

    let atleast_one_checkmark_ticked = variables_for_summary["atleast_one_checkmark_ticked"]
    if(atleast_one_checkmark_ticked==false){
    alert("No Contextsize was selected");
    return;
    }

    let response_json;

    // Disable Analyse Button while function is calculating and styling
    let analyse_button = document.getElementById("calculate_button");
    let loader = document.getElementById("load");

    close_button_show_loader(analyse_button,loader);

    //Send Data to Backend and await calculated results
    await fetch("http://127.0.0.1:5000/summarize", 
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body:JSON.stringify(variables_for_summary)
        }).then( (response) =>{
            if(response.ok){
                //alert(response.json());
                //It returns a promise which resolves with the result of parsing the body text as JSON
                return response.json();
            }else{
                alert("something is wrong" + response.toString());
            }
        }).then(jsonResponse=>{

            o = JSON.stringify(jsonResponse);
            
            response_json = jsonResponse
        }).catch((err) => console.error(err));

    //Hide loading circle; Enable Analyse Button when function is finished
    open_button_hide_loader(analyse_button,loader);

    let main_Container = document.getElementById("Summary");

    let new_summary = document.createElement("p");
    new_summary.setAttribute('id', "new_summary");

    new_summary.setAttribute('align', "left");

    draw_diagramm(response_json);

    //Add each sentence of the summary with space between them
    for(let i = 0; i < response_json["sentences"].length; i++){
        new_summary.innerHTML += response_json["sentences"][i] + " ";
    }

    main_Container.append(new_summary);
}

function draw_diagramm(response_json){
    // Diagramm
    labels = [];
    values = [];
    data = [];
    labelsZusammenfassung = [];
    valuesZusammenfassung = [];
    dataZusammenfassung = [];

    // Häufigkeit aller Daten wird zu einem Datenobjekt verarbeitet
    for(let i = 0; i < response_json["timestampsforDiagramm"].length; i++){
        labels.push(response_json["timestampsforDiagramm"][i]);
    }

    for(let i = 0; i < response_json["occurrencesforDiagramm"].length; i++){
        values.push(response_json["occurrencesforDiagramm"][i]);
    }

    for(let i = 0; i < labels.length; i++){

        const points = {x:labels[i],y:values[i]}
        data.push(points);
    }

    // Formatierung der für die Zusammenfassung genutzten Daten
    for(let i = 0; i < response_json["timestamp"].length; i++){
        if(labelsZusammenfassung.includes(response_json["timestamp"][i])){
            valuesZusammenfassung[i] = valuesZusammenfassung[i] + 1;
        }
        else{
            labelsZusammenfassung.push(response_json["timestamp"][i]);
            valuesZusammenfassung.push(1);
        }
    }

    for(let i = 0; i < labelsZusammenfassung.length; i++){

        const points = {x:labelsZusammenfassung[i],y:valuesZusammenfassung[i]}
        dataZusammenfassung.push(points);
    }

    var mychartObject = document.getElementById('myChart')

    /*
    var chart = new Chart(mychartObject, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Alle Daten",
                backgroundColor: 'rgba(65,105,225,1)',
                borderColor: 'rgba(65,105,225,1)',
                data: values
            }, {
            label: "Daten der Zusammenfassung",
            backgroundColor: 'rgba(12,55,225,1)',
            borderColor: 'rgba(12,55,225,1)',
            data: [{x:'2013-01-16T16:54:22.0Z', y:20}, {x:'2013-01-17T14:57:20.0Z', y:10}]
            }]
        }
    });
    */
   
    var chart = new Chart(mychartObject, {
        type: 'bar',
        data: {
            datasets: [{
                label: "Alle Daten",
                backgroundColor: 'rgba(65,105,225,1)',
                borderColor: 'rgba(65,105,225,1)',
                data: data
            }, {
                label: "Zusammenfassung Daten",
                backgroundColor: 'rgba(255,0,0,1)',
                borderColor: 'rgba(255,0,0,1)',
                data: dataZusammenfassung
            }],
        },
        options: {
            legend: {
              display: false
            },
            scales: {
              yAxes: [{
                ticks: {
                  display: false,
                },        
                gridLines: {
                  display: false
                }
              }],
              xAxes: [{
                type: 'time',
                time: {
                  unit: 'hour',
                  tooltipFormat: 'MMM DD',
                },
                gridLines: {
                  display:false
                }
              }]
            }
          }
      });
  
  }

function get_parameter_as_json(){

    let dataset = document.getElementById("type_of_dataset").value
    if(!dataset){dataset = "empty"}

    let max_length = document.getElementById("max_length").value;
    if(!max_length){max_length = 600}

    let date_from = document.getElementById("date_from").value;
    let time_from = document.getElementById("time_from").value;

    let date_to = document.getElementById("time_from").value;
    let time_to = document.getElementById("time_from").value;

    let function_type = document.getElementById("type_of_function").value;

    // Check if Parameters have been entered
    let summary_question = document.getElementById("text_area").value;
    if(!summary_question){summary_question = ""}

    let exclude_params = document.getElementById("text_area_exclude").value;
    if(!exclude_params){exclude_params = ""}

    //Get Value for checkmarks Kontext
    let kontext_mark_one = document.getElementById("kontext_eins").checked;
    let kontext_mark_two = document.getElementById("kontext_zwei").checked;
    let kontext_mark_three = document.getElementById("kontext_drei").checked;
    let kontext_mark_four = document.getElementById("kontext_vier").checked;

    let list_of_checks = [kontext_mark_one,kontext_mark_two,kontext_mark_three,kontext_mark_four]; 
    //Validate if atleast one has been ticked
    let atleast_one = false;
    for(let j = 0; j<list_of_checks.length;j++){
        if (list_of_checks[j] === true) {
            atleast_one = true;
            }
    }

    let checkmark_likes = document.getElementById("likes").checked;
    let checkmark_follows = document.getElementById("follows").checked;

    let number_concepts = document.getElementById("numb_concepts").value
    let order_of_summary = document.getElementById("type_of_summary_return").value

    // Make a json with all parameters, to be send to the backend
    let variables_for_summary = {
                                "max_length": max_length,
                                "question": summary_question,
                                "exclude_params":exclude_params,
                                "timespan" : {"from": {"date":date_from, "time":time_from}, "to": {"date": date_to, "time":time_to}},
                                "function_type": function_type,
                                "dataset":dataset,
                                "atleast_one_checkmark_ticked":atleast_one,
                                "kontext_checkmarks": {"eins":kontext_mark_one,"zwei":kontext_mark_two,"drei":kontext_mark_three,"vier":kontext_mark_four},
                                "meta_daten":{"likes":checkmark_likes,"follow":checkmark_follows},
                                "number_of_concepts": number_concepts,
                                "return_order_of_summary":order_of_summary,    
                            };
    //alert(JSON.stringify(variables_for_summary))
    return variables_for_summary;
}

/**
 * Shows the loading circle animation when the "Analyse" button is pressed
 * 
 * @param {analyse_button} analyse_button is the Button "Analyse"
 * @param {loader} loader is the loading circle including the animation in css
 * 
 * @note Also makes the Button "Analyse" unclickable and grayed out
 */
function close_button_show_loader(analyse_button,loader){
    analyse_button.style.opacity = 0.5
    analyse_button.style.cursor = "not-allowed"
    analyse_button.disabled = true

    //Show loading Cricle animation
    loader.style.animation = "spin 2s linear infinite"
    loader.style.visibility = "visible"
}

/**
 * Hides the loading circle Animation when the summary is returned from the back-end
 * 
 * @param {analyse_button} analyse_button is the Button "Analyse"
 * @param {loader} loader is the loading circle including the animation in css
 * 
 * @note Also makes the Button "Analyse" clickable and no longer grayed out
 */
function open_button_hide_loader(analyse_button,loader){
    loader.style.visibility = "hidden"
    loader.style.animation = ""
    analyse_button.style.cursor = ""
    analyse_button.style.opacity = 1
    analyse_button.disabled = false;
}