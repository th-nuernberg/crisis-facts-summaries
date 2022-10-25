/***
 * When entering/refreshing the Website
 * Add Eventlistener to the Button "Analyse" ->  for Function "make_a_summary"
 * Add Eventlistener to the Button "More Options" -> make it into a collapsible Dropdown menu
 */
function initAssignment(){

    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)

    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            // add the functinality to make the "more options" button into a dropdown menu
            this.classList.toggle("active");
            var content = document.getElementById("field_more_opt");
            if (content.style.maxHeight){
            content.style.maxHeight = null;
            } else {
            content.style.maxHeight = content.scrollHeight + "px";
            } 
        });}
}


/**
 * When entering/refreshing the Website
 * Make a Get Request to the Backend to the address "http://127.0.0.1:5000/datasets"
 * 
 * @note the return Value of this adress is a json format string and includes filenames
 *       that are in the folder: "website/Data/Datensaetze/prepared" and end with json or jsonl
 * 
 * Add every name in the json string as option for the dropdown menu "Dataset to analyse"
 * 
 * @note for the function that gets the datasets see the file: "website/Data/app.py"
 */
async function getDataset(){

    let response_json;

//#region Get request to the backend to the adress "http://127.0.0.1:5000/datasets"

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

//#endregion

        //Create the options for the dropdown menu
        let data_dropdown = document.getElementById("type_of_dataset");
        
        for(let i = 0; i < response_json["files"].length; i++){
            let new_option = document.createElement("option");
            new_option.setAttribute('class',"dropbtn_opt");
            new_option.setAttribute('value',response_json["files"][i]);
            new_option.innerHTML=response_json["files"][i];
            data_dropdown.appendChild(new_option);
        }    
}

/**
 * When pressing the Button "Analyse"
 * Remove previous html element with a summary if it exists
 * 
 * Call Function get_parameter_as_json(): to get all front_end Parameters 
 * Check if atleast one Contextsize was selected
 * @note if none were selected: cancel the function | else: proceed as usual
 * 
 * Call Function close_button_show_loader(): so no further request can be made till the first one is done
 * 
 * Make a abort Controller for a timeout function with variable timer
 * 
 * Make a Post Request to the Backend to the address "http://127.0.0.1:5000/summarize" with front_end parameters
 * @note the return Value of this adress is a json format string and includes the summary and the timestamps
 * 
 * Create a new html element with the Parameters from the json file
 * 
 * Call Function open_button_hide_loader: Enable the Button "Analyse"
 * 
 * Call Function "Draw_Diagramm()"
 * 
 * @note for the function that summarizes see the file: "website/Data/app.py"
 */
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

    //make a controller for a timeout if Backend takes to long
    const controller = new AbortController();
    const timeoutID = setTimeout(() => controller.abort(), variables_for_summary["time_till_timeout_in_ms"])

//#region Post request to the backend to the adress "http://127.0.0.1:5000/summarize"

    //Send Data to Backend and await calculated results
    await fetch("http://127.0.0.1:5000/summarize", 
        {
            signal: controller.signal,
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
//#endregion

    //Hide loading circle; Enable Analyse Button when function is finished
    open_button_hide_loader(analyse_button,loader);

//#region create the new html element with the sentences from the json as innerHTML and append to the Summary

    let main_Container = document.getElementById("Summary");
    let new_summary = document.createElement("p");
    new_summary.setAttribute('id', "new_summary");

    new_summary.setAttribute('align', "left");

    //Add each sentence of the summary with space between them
    for(let i = 0; i < response_json["sentences"].length; i++){
        new_summary.innerHTML += response_json["sentences"][i] + " ";
    }
    main_Container.append(new_summary);

//#endregion

    draw_diagramm(response_json);
}

/**
 * After execution of function make_a_summary()
 * Draws a diagramm wich shows on wich timestamps how many information nuggets were extracted
 * 
 * Extracts all timestamps from the Json string
 * Checks if timestamp occurs more than once
 * @note if timestamp occurs more than once the value entry will be changed
 * 
 * All labels and values are saved in a data array
 * 
 * The same procedure follows for the timestamps of the selected sentences 
 * 
 * After all timetstamps are saved in data arrays the chart object will be created
 * 
 * In this object, two datasets will be configured. One for all timestamps and one for the timestamps of the selected sentences
 * 
 * Two add-ons / plugins are implemented 
 * 
 * First the time-adapter (to display the time on the timeline correctly)
 * 
 * Last the zoom-plugin (so you can zoom in the diagramm)
 */
function draw_diagramm(response_json){
    
//#region Initialize all variables
    labels = [];
    values = [];
    data = [];
    labelsZusammenfassung = [];
    valuesZusammenfassung = [];
    dataZusammenfassung = [];
//#endregion

//#region all timestamps are packed into data[]
    for(let i = 0; i < response_json["timestampsforDiagramm"].length; i++){
        timestamp_not_formatted = response_json["timestampsforDiagramm"][i];
        timestamp = timestamp_not_formatted.slice(0,10); // timestamps are formatted into the right format
        wasset = false;
        
        if(labels.length == 0){}
        else
        {
            for(let j in labels)
            {
                if(labels[j] == timestamp){
                    values[j] = values[j] + 1;
                    wasset = true;
                }
            }
        }

        if(wasset == false)
        {
            labels.push(timestamp);
            values.push(1);
        }
    }

    for(let i = 0; i < labels.length; i++){

        const points = {x:labels[i],y:values[i]}
        data.push(points);
    }
//#endregion

//#region only the timestamps wich belong to the selected sentences are packed into an own dataZusammenfassung[] array
    for(let i in response_json["timestamp_dict"]){
        timestamp_not_formatted = i;
        timestamp = timestamp_not_formatted.slice(0,10);// timestamps are formatted into the right format
        wasset = false;
        
        if(labelsZusammenfassung.length == 0){}
        else
        {
            for(let j in labelsZusammenfassung)
            {
                if(labelsZusammenfassung[j] == timestamp){
                    valuesZusammenfassung[j] = valuesZusammenfassung[j] + 1;
                    wasset = true;
                }
            }
        }

        if(wasset == false)
        {
            labelsZusammenfassung.push(timestamp);
            valuesZusammenfassung.push(1);
        }
    }

    for(let i = 0; i < labelsZusammenfassung.length; i++){

        const points = {x:labelsZusammenfassung[i],y:valuesZusammenfassung[i]}
        dataZusammenfassung.push(points);
    }
//#endregion

//#region creation of a new chart
    var mychartObject = document.getElementById('myChart')
    var chart = new Chart(mychartObject, {
        data: {
            datasets: [{
                type: 'bubble',
                label: "Summary Timestamps",
                backgroundColor: 'rgba(255,0,0,1)',
                borderColor: 'rgba(255,0,0,1)',
                data: dataZusammenfassung
            }, {
                type: 'line',
                label: "All Timestamps",
                backgroundColor: 'rgba(65,105,225,1)',
                borderColor: 'rgba(65,105,225,1)',
                data: data
            }],
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero :true
                }
            },
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true,
                        },
                        pinch: {
                            enabled: true
                        },
                        mode: 'x',
                    }
                }
            }
        }       
    },)
//#endregion

}


/**
 * When called by the function make_a_summary()
 * gets the values of the front end Parameter and makes a json string
 * 
 * @note also adds a paramter in the json file if atleast one of the Checkboxes for 
 * Kontextsize was checked
 * 
 * @return all parameters from the front End GUI as a json formated string
 */
function get_parameter_as_json(){
    
//#region Get Parameters outside of the more options field
    let dataset = document.getElementById("type_of_dataset").value
    if(!dataset){dataset = "empty"}
    
    let max_length = document.getElementById("max_length").value;

    let date_from = document.getElementById("date_from").value;
    let time_from = document.getElementById("time_from").value;

    let date_to = document.getElementById("date_to").value;
    let time_to = document.getElementById("time_to").value;

    let function_type = document.getElementById("type_of_function").value;

    let represent_type = document.getElementById("type_of_representation").value
//#endregion

    // Check if Keywords have been entered in search or exclude
    let summary_question = document.getElementById("text_area").value;
    if(!summary_question){summary_question = ""}

    let exclude_params = document.getElementById("text_area_exclude").value;
    if(!exclude_params){exclude_params = ""}

//#region Get Checkbox Params in more options and check if atleast one was clicked
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
//#endregion


//#region Get Parameters in the more options field
    let number_concepts = document.getElementById("numb_concepts").value;
    let order_of_summary = document.getElementById("type_of_summary_return").value;

    let min_df = document.getElementById("min_df").value;
    let max_df = document.getElementById("max_df").value;

    let use_stopword_list = document.getElementById("stopword_checkbox").checked;

    let weight_search_param = document.getElementById("weight_search_param").value;
    let weight_exclude_param = document.getElementById("weight_exclude_param").value;

    let hard_exclude = document.getElementById("hard_exclude").checked;

    let time_till_timeout_in_ms = document.getElementById("time_till_timeout").value;
    time_till_timeout_in_ms = time_till_timeout_in_ms*60*1000;
//#endregion

    // Make a json with all parameters, to be send to the backend
    let variables_for_summary = {
                                "max_length": max_length,
                                "question": summary_question,
                                "exclude_params":{"params":exclude_params,"hard_exclude":hard_exclude},
                                "timespan" : {"from": {"date":date_from, "time":time_from}, "to": {"date": date_to, "time":time_to}},
                                "function_type": function_type,
                                "dataset":dataset,
                                "represent_type": represent_type,
                                "atleast_one_checkmark_ticked":atleast_one,
                                "kontext_checkmarks": {"eins":kontext_mark_one,"zwei":kontext_mark_two,"drei":kontext_mark_three,"vier":kontext_mark_four},
                                "number_of_concepts": number_concepts,
                                "return_order_of_summary":order_of_summary,
                                "tf_idf":{"min_df":min_df, "max_df":max_df},
                                "use_stopwordlist":use_stopword_list,
                                "weight_of_params":{"include": weight_search_param, "exclude": weight_exclude_param, },
                                "time_till_timeout_in_ms": time_till_timeout_in_ms,    
                            };
    //alert(JSON.stringify(variables_for_summary))  //for debugging
    return variables_for_summary;
}

/**
 * When Called by the function make_a_summay()
 * Show the loading circle animation
 * 
 * @note Also makes the Button "Analyse" unclickable and grayed out
 * 
 * @param {analyse_button} analyse_button is the Button "Analyse"
 * @param {loader} loader is the loading circle including the animation in css
 * 
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
 * When Called by the function make_a_summay() when it gets a answer from the back_end
 * Hide the loading circle Animation
 * 
 * @note Also makes the Button "Analyse" clickable and no longer grayed out
 * 
 * @param {analyse_button} analyse_button is the Button "Analyse" in the front end GUI
 * @param {loader} loader is the loading circle including the animation in css
 * 
 */
function open_button_hide_loader(analyse_button,loader){
    loader.style.visibility = "hidden"
    loader.style.animation = ""
    analyse_button.style.cursor = ""
    analyse_button.style.opacity = 1
    analyse_button.disabled = false;
}