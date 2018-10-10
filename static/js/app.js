var module = angular.module("statsApp", ['ngRoute']);
module.config(function ($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

module.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.when('/route1', {
            templateUrl: static_url + 'partials/test1.html',
            controller: 'RouteController1'
        }).when('/route2', {
            templateUrl: static_url + 'partials/test2.html',
            controller: 'RouteController2'
        }).when('/createDataset', {
            templateUrl: static_url + 'partials/newdataset.html',
            controller: 'createNewDataset'
        }).when('/createProcess', {
            templateUrl: static_url + 'partials/newprocess.html',
            controller: 'processCtrl'
        }).when('/datasetList', {
            templateUrl: static_url + 'partials/datasetListing.html',
            controller: 'datasetListCtrl'
        }).when('/chart', {
            templateUrl: static_url + 'partials/chart.html',
            controller: 'RouteController1'
        }).when('/upload1', {
            templateUrl: static_url + 'partials/dataset_upload.html',
            controller: 'RouteController1'
        }).when('/createVisual', {
            templateUrl: static_url + 'partials/visualization.html',
            controller: 'visualizationCtrl'
        }).when('/visualList', {
            templateUrl: static_url + 'partials/visualizationList.html',
            controller: 'visualizationListCtrl'
        }).when('/dashboard', {
            templateUrl: static_url + 'partials/dashboard.html',
            controller: 'dashboardCtrl'
        }).when('/csv', {
            templateUrl: static_url + 'partials/uploadManually.html',
            controller: 'RouteController5'
        }).when('/statisticalList', {
            templateUrl: static_url + 'partials/statisticalList.html',
            controller: 'statisticalListCtrl'
        }).when('/statistical', {
            templateUrl: static_url + 'partials/statistical.html',
            controller: 'statisticalCtrl'
        }).when('/analytical', {
            templateUrl: static_url + 'partials/analytical.html',
            controller: 'analyticalCtrl'
        }).when('/analyticalList', {
            templateUrl: static_url + 'partials/analyticalList.html',
            controller: 'analyticalListCtrl'
        }).when('/mlearn', {
            templateUrl: static_url + 'partials/mlearn.html',
            controller: 'mlearnCtrl'
        });
    }]);




//AnalyticalList controller
module.controller("analyticalListCtrl",function($scope,$http){
    $scope.analyticalArr = [];
    $scope.analyticalName = '';
    let url = '/getAnalytical/';
    $http.get(url)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.analyticalArr = response.data;

        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.refreshList = function () {
        $http.get(url)
            .then(function (response) {
                //First function handles success
                console.log("get response", response);
                $scope.analyticalArr = response.data;

            }, function (response) {
                //Second function handles error
                console.log("Something went wrong");
            });
    }

    $scope.viewAnalytical = function (statistical) {
		$scope.selMethod = statistical.analytical_method;
        console.log("in view",statistical);
        console.log("selectedfield",statistical.analytical_method);
        console.log("selectedmethod",$scope.selMethod);
        console.log("json summary", statistical.analytical_calculated_value);
        $scope.calSummary = JSON.parse(statistical.analytical_calculated_value);
        $scope.selMethod = statistical.analytical_method;

        // console.log("vParams", visualization.parameters.labels);
        // console.log("vParams1", visualization.parameters.defaultData);
        // xdata = visualization.parameters.labels;
        // ydata = visualization.parameters.defaultData;
        // gType = visualization.type;
        // divId = document.getElementById("chartView");
        // console.log("divId", divId.id);
        // viewChart(xdata, ydata, divId.id);
    }

    $scope.delAnalytical = function (analyticalId) {
        let url = '/delAnalytical/' + analyticalId + '/';
        $http.delete(url)
            .success(function (data, status, headers) {
                console.log("in delete analytical http", data);
                if (data === 'delete successful') {
                    location.reload();
                }
                else {
                    alert("Analytical Summary is not deleted successfully");
                }

            })
            .error(function (data, status, header, config) {
                console.log("something went wrong");
            });

    }
    $scope.test ="This is working analyticalList";

});


module.controller("statisticalListCtrl",function($scope,$http){
     $scope.statisticalArr = [];
    $scope.statisticalName = '';
    let url = '/getStatistical/';
    $http.get(url)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.statisticalArr = response.data;

        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.refreshList = function () {
        $http.get(url)
            .then(function (response) {
                //First function handles success
                console.log("get response", response);
                $scope.statisticalArr = response.data;

            }, function (response) {
                //Second function handles error
                console.log("Something went wrong");
            });
    }

    $scope.viewStatistical = function (statistical) {
		$scope.selMethod = statistical.statistical_method;
        console.log("in view",statistical);
        console.log("selectedfield",statistical.statistical_method);
        console.log("selectedmethod",$scope.selMethod);
        console.log("json summary", statistical.statistical_calculated_value);
        $scope.calSummary = JSON.parse(statistical.statistical_calculated_value);
        $scope.selMethod = statistical.statistical_method;

        // console.log("vParams", visualization.parameters.labels);
        // console.log("vParams1", visualization.parameters.defaultData);
        // xdata = visualization.parameters.labels;
        // ydata = visualization.parameters.defaultData;
        // gType = visualization.type;
        // divId = document.getElementById("chartView");
        // console.log("divId", divId.id);
        // viewChart(xdata, ydata, divId.id);
    }

    $scope.delStatistical = function (statisticalId) {
        let url = '/delStatistical/' + statisticalId + '/';
        $http.delete(url)
            .success(function (data, status, headers) {
                console.log("in delete statistical http", data);
                if (data === 'delete successful') {
                    location.reload();
                }
                else {
                    alert("Statistical Summary is not deleted successfully");
                }

            })
            .error(function (data, status, header, config) {
                console.log("something went wrong");
            });

    }
    $scope.test ="This is working statisticalList";

});


module.controller("statisticalCtrl", function($scope,$http) {
    $scope.test ="This is working statistical";
    $scope.calculationDone = false;
    $scope.methodArr = ['describe'];
    $scope.selectedfield = '';
    $scope.selectedmethod = '';
    let selDatasetId = '';
    let fieldDataToSave = '';

    $scope.showGraph1 = false;
    //console.log('sdsdfgsdfgfdg');
    let url = '/getDataset/'
    $http.get(url)
        .then(function (response) {
            //First function handles success
            $scope.datasetArr = response.data;
        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.choiceDataset =function(x){
        dataset = $scope.datasetArr;
        console.log("dataset==>", dataset);
        let dashall  = _.find(dataset, function(o) { return o.dataset === x; });
        console.log("DATASNAME", dashall);

        }
    $scope.chooseDataset = function (dataset) {
        console.log("datasetselection",dataset);
        selDatasetId = dataset.dataset_id;
        $scope.selectedDataset = dataset.dataset_name;
        $scope.sName = '';
        let data = new FormData();
        let url = '/getGraphFields/';
        data.append("dName", dataset.dataset_name);

        $http.post(url, data, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            $scope.fieldsAr = data;
            console.log("fieldsAr", $scope.fieldsAr);
            $scope.showGraph1 = true;
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("somethingvName went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }




    $scope.calculateStatistical = function () {
     //   console.log('####selectedfield',$scope.selectedfield);
     //   console.log('#####selectedmethod',$scope.selectedmethod);

        let url='/calculateStatistics/';
        let dt = new FormData();
        dt.append("dataset_id", selDatasetId);
    //    console.log('dataset_id',selDatasetId);
        dt.append("selectedfield", $scope.selectedfield);
        dt.append("selectedmethod",$scope.selectedmethod);

        $http.post(url,dt,{
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function(data,status,headers,config){
         //   $scope.fieldsAr = data;
            console.log("response from calculateStatistics",data);


             if($scope.selectedmethod == 'mode'){
                     $scope.calculatedSummary =  data.summary;
                     $scope.calculationDone = true;
                     fieldDataForoGraph = data.fieldData;
                     fieldDataToSave = fieldDataForoGraph.toString();

             }
             else if($scope.selectedmethod == 'describe'){
                     $scope.calculatedSummary =  data.summary;
                     $scope.calculationDone = true;
                     fieldDataForoGraph = data.fieldData;
                     fieldDataToSave = fieldDataForoGraph.toString();
                     var trace = {
    					x: fieldDataForoGraph,
    					type: 'histogram',
  						};
						var data = [trace];
						Plotly.newPlot('histoDiv', data);

             		}

        }).error(function(data,status,headers,config){
            console.log("Something went wrong");
        });

    }

    $scope.initCalculate = function(){
        $scope.calculationDone = false;
    }

    $scope.paramterSave1 = function () {
        console.log("Hiiiiiiiii");
        // let graphData = {
        //     "labels": labels,
        //     "defaultData": defaultData
        // };
        let url = '/saveStatistics/';
        let dt = new FormData();
        dt.append("statistical_name", $scope.sName);
        // dt.append("data", JSON.stringify(graphData));
        dt.append("dataset_id", selDatasetId);
        dt.append("selectedfield",$scope.selectedfield);
        dt.append("selectedmethod",$scope.selectedmethod);
        dt.append("fieldData",fieldDataToSave);
        dt.append("statistical_calculated_value",JSON.stringify($scope.calculatedSummary));
		console.log("JDATA======>",JSON.stringify($scope.calculatedSummary));


        console.log("Hi from statistical");
        console.log("$$$$$$$",typeof($scope.calculatedSummary));

        console.log("val to save",$scope.calculatedSummary);
        // dt.append("graphType", graphType);
        // console.log('graphy', graphData);

        $http.post(url, dt, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            if (data == "saved successfully") {
                $('#successModal').modal();
            }
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });


    }
});

module.controller("mlearnCtrl",function($scope,$http){
	$scope.mlearnArr = [];
	$scope.mlearnName = '';
	$scope.test ="This is working mlearn";
    $scope.selectdata = [$scope.mlearnArr];

    $scope.selecteddataset = '';

	console.log("Inside mLearn");
	let url = '/getDataset/'
    $scope.eminem = false;
    $scope.venom = false;
    $http.get(url)
        .then(function (response) {
            //First function handles success
            $scope.mlearnArr = response.data;
            var value1;
			console.log("SCOPE.DATSETARR", $scope.mlearnArr);
			$('select[name="dataset"]').change(function(){
				var e1 = document.getElementById("dataset");
				value1 = e1.options[e1.selectedIndex].value;
                var e2 = document.getElementById("algo");
				value2 = e2.options[e2.selectedIndex].value;


                console.log("VALUE",value1);
                console.log("VALUE2",value2);

                let x;
                let dashall = _.findIndex(response.data, function(o) { return o.dataset_name === value1; });

                console.log("DATASETINDEX", dashall);
                dset = response.data[dashall];

                console.log("selected dataset",dset);
			});
            $('select[name="algo"]').change(function(){
                var e2 = document.getElementById("algo");
				value2 = e2.options[e2.selectedIndex].value;


                console.log("VALUE2",value2);

			});


        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });
        $scope.chooseDataset = function () {
            selDatasetId = dset.dataset_id;
            selAlgoId = value2;
            console.log("ALGOOOOO", selAlgoId);
    		console.log("#####", selDatasetId);
            $scope.selectedDataset = dset.dataset_name;
            console.log("selectedDataset", $scope.selectedDataset);
            $scope.aName = '';
            let data = new FormData();
            let url = '/getGraphFields/';
            data.append("dName", dset.dataset_name);
            console.log(dset.dataset_name);
            console.log("data", data);
            $http.post(url, data, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                $scope.fieldsAr = data;

                $scope.eminem = true;
                $('select[name="idvar"]').change(function(){
                    var idvar = document.getElementById("idvar");
    				idvar = idvar.options[idvar.selectedIndex].value;
                    var dvar = document.getElementById("dvar");
    				dvar = dvar.options[dvar.selectedIndex].value;
                    var but = document.getElementById("slct-btn2");
                    if(idvar == dvar){
                        but.disabled = true;
                    }
                    else{
                        but.disabled = false;
                    }



                });
                $('select[name="dvar"]').change(function(){
                    var idvar = document.getElementById("idvar");
    				idvar = idvar.options[idvar.selectedIndex].value;
                    var dvar = document.getElementById("dvar");
    				dvar = dvar.options[dvar.selectedIndex].value;
                    var but = document.getElementById("slct-btn2");
                    if(idvar == dvar){
                        but.disabled = true;
                    }
                    else{
                        but.disabled = false;
                    }
                    console.log("DVAR_VAL", dvar);
                    console.log("IDVAR_VAL", idvar);
                });
                // this callback will be called asynchronously
                // when the response is available
            }).error(function (data, status, headers, config) {
                console.log("somethingvName went wrong");

                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });

        }

        $scope.chooseVariables = function(){
            let url = '/calcsregression/';
            console.log("insidechoosevar");
            $http.get(url)
                .then(function (response) {
                    //First function handles success
                    $scope.venom = true;
                }, function (response) {
                    //Second function handles error
                    console.log("Something went wrong");
                });
        }

        $scope.selectparm = function(){
            $scope.training_size='';
            $scope.random_state='';
            $scope.fit_intercept='';
            selDatasetId = dset;
            console.log("selectparm");
            selDatasetId = dset.dataset_id;
            selAlgoId = value2;
            $scope.selectedDataset = dset.dataset_name;
            $scope.aName = '';
            let data = new FormData();
            let url = '/getGraphFields/';
            let url2='/calcsregression/';
            let dt = new FormData();
            data.append("dName", dset.dataset_name);
            data.append("training_size",training_size);
            data.append("random_state", random_state);
            data.append("fit_intercept", fit_intercept);
            $http.post(url2,data,{
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data,status,headers,config) {
                    //First function handles success
                    let sara = new FormData();
                    var t_size = document.getElementById("training_size").value;
                    sara.append("training_size",t_size);
                    console.log("DT====>",sara);
                    console.log("insidecalcregression");
                }). error(function (data,status,headers,config) {
                    //Second function handles error
                    console.log("Something went wrong");
                });
            $http.post(url, data, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                $scope.fieldsAr = data;
                console.log("lalala");
                $(function(){
                    var t_size = document.getElementById("training_size").value;
                    var r_state = document.getElementById("random_state").value;
                    var f_intercept = document.getElementById("fit_intercept").value;
                    console.log("training_size",t_size);
                    $scope.training_size = t_size;
                    dt = new FormData();
                    var a =dt.append("training_size",t_size);

                    console.log("random_state",r_state);
                    console.log("fit_intercept",f_intercept);

                });

                // this callback will be called asynchronously
                // when the response is available
            }).error(function (data, status, headers, config) {
                console.log("somethingvName went wrong");

                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });

        }

	$scope.testc =function(dataset){
        dataset = $scope.mlearnArr;
        console.log("dataset==>", dataset);
        let dashall  = _.find(dataset, function(o) { return o.dataset === x; });
        console.log("DATASNAME", dashall);


        }

	});

module.controller("analyticalCtrl", function($scope,$http) {
    $scope.test ="This is working analytical";
    $scope.calculationDone = false;
    $scope.methodArr = ['anova'];
    $scope.selecteddatacol = '';
    $scope.selectedgroup = '';
    $scope.selectedmethod = '';
    let selDatasetId = '';
    let fieldDataToSave = '';

    $scope.showGraph1 = false;
    //console.log('sdsdfgsdfgfdg');
    let url = '/getDataset/'
    $http.get(url)
        .then(function (response) {
            //First function handles success
            $scope.datasetArr = response.data;
        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });
    $scope.chooseDataset = function (dataset) {
        selDatasetId = dataset.dataset_id;

		console.log("#####", selDatasetId);
        $scope.selectedDataset = dataset.dataset_name;
        $scope.aName = '';
        let data = new FormData();
        let url = '/getGraphFields/';
        data.append("dName", dataset.dataset_name);
        $http.post(url, data, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            $scope.fieldsAr = data;
            console.log("fieldsAr", $scope.fieldsAr);
            $scope.showGraph1 = true;
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("somethingvName went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }




    $scope.calculateAnalytical = function () {
     //   console.log('####selectedfield',$scope.selectedfield);
     //   console.log('#####selectedmethod',$scope.selectedmethod);

        let url='/calculateAnalytics/';
        let dt = new FormData();
        dt.append("dataset_id", selDatasetId);
    //    console.log('dataset_id',selDatasetId);
        dt.append("selecteddatacol", $scope.selecteddatacol);
        dt.append("selectedgroup", $scope.selectedgroup);
        console.log("dfbdfjd nfdnbf", $scope.selectedgroup);
        dt.append("selectedmethod",$scope.selectedmethod);

        $http.post(url,dt,{
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function(data,status,headers,config){
          console.log("response from calcula",data);
            console.log("response from calculateAnalytics",data);
			 console.log("response calculateAnalytics");


             if($scope.selectedmethod == 'mode'){
                     $scope.calculatedSummary =  data.summary;
                     $scope.calculationDone = true;
                     fieldDataForoGraph = data.fieldData;
                     fieldDataToSave = fieldDataForoGraph.toString();

             }
             else if($scope.selectedmethod == 'anova'){
                     $scope.calculatedSummary =  data.summary;
                     $scope.calculationDone = true;
                 //    fieldDataForoGraph = data.fieldData;
                   //  fieldDataToSave = fieldDataForoGraph.toString();
				     console.log("In else calculateAnalytics",data);
					   console.log("calculatedSummary calculateAnalytics",$scope.calculatedSummary);

				}
		}).error(function(data,status,headers,config){
            console.log("Something went wrong");
        });

    }

    $scope.initCalculate = function(){
        $scope.calculationDone = false;
    }

    $scope.paramterSave2 = function () {
        console.log("Hiiiiiiiii");
        // let graphData = {
        //     "labels": labels,
        //     "defaultData": defaultData
        // };
        let url = '/saveAnalytics/';
        let dt = new FormData();
        dt.append("analytical_name", $scope.aName);
        // dt.append("data", JSON.stringify(graphData));
        dt.append("dataset_id", selDatasetId);
        dt.append("selectedgroup",$scope.selectedgroup);
        dt.append("selecteddatacol",$scope.selecteddatacol);
        dt.append("selectedmethod",$scope.selectedmethod);
        dt.append("fieldData",fieldDataToSave);
		console.log("JDATA======>",JSON.stringify($scope.calculatedSummary));
        dt.append("analytical_calculated_value",JSON.stringify($scope.calculatedSummary));
		console.log("HI from analytic");
		console.log("&&&&&&&", typeof($scope.calculatedSummary));
        console.log("val to save",$scope.calculatedSummary);
        // dt.append("graphType", graphType);
        // console.log('graphy', graphData);

        $http.post(url, dt, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            if (data == "saved successfully") {
                $('#successModal').modal();
            }
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });


    }
});




module.controller("dashboardCtrl", function ($scope,$http) {
    $scope.test = "This is working test1";
    $scope.selectedVisual = '';
    $scope.isNameSaved = true;
    $scope.dashboardName = 'none';
    $scope.isDashboardVisible = false;
    let visualizationInDashId = '';
    let textNarration = 'Write some narration for this graph';
    let gType = '';
    let xData = [];
    let yData = [];
    let vurl = '/getVisualization/';
    $http.get(vurl)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.vList = response.data;

        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.saveDashboardName = function(){
        $scope.isNameSaved = true;
    }
    $scope.editDashboardName = function(){
        $scope.isNameSaved = false;
    }

    $scope.addVisual = function(btnId){
        console.log("button id", btnId.target.id);
        let id = btnId.target.parentNode.id;
        console.log("button id", btnId.target.parentNode);
        let parent = btnId.target.parentNode;
        let canvas = document.createElement("canvas");
        let div = document.createElement("div");
        let testdiv = document.getElementById("testdiv");
        div.className = "col-md-12 my-4";
        visualizationInDashId = "vId" + id;
        canvas.id = visualizationInDashId;
        canvas.width = 1000;
        canvas.height = 300;
       // div.appendChild(canvas);
        div.appendChild(canvas);
        parent.appendChild(div);

        document.getElementById(btnId.target.id).style.display = 'none';


    }

    $scope.initDashboard = function(){
        $scope.isDashboardVisible = true;
    }

    function viewChart(x, y, id) {
        var ctx2 = document.getElementById(id);
        xData = x;
        yData = y;
        var myChart = new Chart(ctx2, {
            type: gType,
            data: {
                labels: x,
                datasets: [{
                    label: '',
                    data: y,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                events: ['click']
            }
        });
    }

    $scope.saveNarration = function(){
        console.log("hi from save narration");
    }
    $scope.openVisualization = function (visualization) {
        let v = _.find($scope.vList, function(o) { return o.visualization_name === visualization; });
        console.log("selected visualization object", v);
        console.log("selected visualization", v);
        console.log("vParams", v.parameters.labels);
        console.log("vParams1", v.parameters.defaultData);
        xdata = v.parameters.labels;
        ydata = v.parameters.defaultData;
        gType = v.type;
        divId = document.getElementById(visualizationInDashId);
        console.log("divId", divId.id);
        let header = document.createElement("h3");
        let t = document.createTextNode("Visualization : " + v.visualization_name);
        header.appendChild(t);
        let parentDiv = divId.parentNode;
        parentDiv.insertBefore(header, parentDiv.childNodes[0]);

        let textArea = document.createElement("input");
        textArea.type = "text";
        textArea.className = "form-control my-4";
        textArea.id = v.visualization_id + "h2";

        textArea.setAttribute("ng-model", $scope.test);
        parentDiv.appendChild(textArea);

        let saveTextBtn = document.createElement("button");
        saveTextBtn.className = "btn btn-primary";
        saveTextBtn.innerText = "Save Sub Title";
        saveTextBtn.setAttribute("ng-model", $scope.test);
        saveTextBtn.onclick = function(){
            console.log("hi from save header", $scope.test);
            let k = document.getElementById(v.visualization_id+"h2").value;
            console.log("conos", k);
            let h2 = document.createElement("h4");
            let h2Val = document.createTextNode(k);
            h2.appendChild(h2Val);
            //parentDiv.appendChild(h2);
            parentDiv.insertBefore(h2, parentDiv.childNodes[2]);
            console.log("this is ans", this.visualization_id);

        }

        let saveNarrationBtn = document.createElement("button");
        saveNarrationBtn.className = "btn btn-primary ml-5";
        saveNarrationBtn.innerText = "Save Narration";
        saveNarrationBtn.setAttribute("ng-model", $scope.test);
        saveNarrationBtn.onclick = function(){
            console.log("hi from save header", $scope.test);
            let k = document.getElementById(v.visualization_id+"h2").value;
            console.log("conos", k);
            let h2 = document.createElement("h4");
            let h2Val = document.createTextNode(k);
            h2.appendChild(h2Val);
            //parentDiv.appendChild(h2);
            console.log("parent ###", parentDiv.children.length);
            parentDiv.insertBefore(h2, parentDiv.childNodes[parentDiv.children.length - 3]);
            console.log("this is ans", this.visualization_id);

        }
        parentDiv.appendChild(saveTextBtn);
        parentDiv.appendChild(saveNarrationBtn);
        $("#myModal").modal("hide");
     //   divId.parentNode.appendChild(header);
        viewChart(xdata, ydata, divId.id);
    }

});

module.controller("RouteController1", function ($scope) {
    $scope.test = "This is working test1"
});
module.controller("RouteController2", function ($scope,$http) {
    $scope.test = "This is working test2"
    $scope.collectionName = '';
    $scope.makeCol = function(){

        let url = '/makeCol/';
        let fm = new FormData();
        fm.append("colName", $scope.collectionName);
        $http.post(url, fm, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");
        });


    }
});

module.controller("visualizationListCtrl", function ($scope, $http) {
    $scope.visualizationArr = [];
    $scope.visualName = '';
    let vurl = '/getVisualization/';
    let ydata = [];
    let xdata = [];
    let gType = '';
    let datasetName = '';
    let xData = [];
    let yData = [];
    let currChartid = '';
    $http.get(vurl)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.visualizationArr = response.data;

        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.refreshList = function () {
        $http.get(vurl)
            .then(function (response) {
                //First function handles success
                console.log("get response", response);
                $scope.visualizationArr = response.data;

            }, function (response) {
                //Second function handles error
                console.log("Something went wrong");
            });
    }

    $(function () {

        $('#create_pdf').click(function () {
            var doc = new jsPDF();
            doc.addHTML($('#viewModalBody')[0], 15, 13, {
                'background': '#fff',
            }, function () {
                doc.save('chart.pdf');
            });
        });
    });

    $scope.createIm = function(){
	//	window.print();
		html2canvas(document.querySelector('.specific'), {
			onrendered: function(canvas) {
			document.body.appendChild(canvas);
				return Canvas2Image.saveAsPNG(canvas);
			}
		});
	}

    function viewChart(x, y, id) {
        var ctx2 = document.getElementById(id);
        xData = x;
        yData = y;
        var myChart = new Chart(ctx2, {
            type: gType,
            data: {
                labels: x,
                datasets: [{
                    label: '',
                    data: y,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                events: ['click']
            }
        });
    }

    $scope.viewVisualization = function (visualization) {
        console.log("vParams", visualization.parameters.labels);
        console.log("vParams1", visualization.parameters.defaultData);
        xdata = visualization.parameters.labels;
        ydata = visualization.parameters.defaultData;
        gType = visualization.type;
        divId = document.getElementById("chartView");
        console.log("divId", divId.id);
        viewChart(xdata, ydata, divId.id);
    }

    $scope.editVisualization = function (chart) {
        console.log("in edit", chart);
        xdata = chart.parameters.labels;
        ydata = chart.parameters.defaultData;
        gType = chart.type;
        currChartid = chart.id;
        divId = document.getElementById("chartEdit");
        viewChart(xdata, ydata, divId.id);
        let durl = '/giveDatasetName/';
        let dform = new FormData();
        dform.append("dataset_id", chart.dataset_id_id);
        $http.post(durl, dform, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            datasetName = data;
            console.log("in edit name", datasetName);
            if (datasetName !== '') {
                getParameters(datasetName);
            }

        }).error(function (data, status, headers, config) {
            console.log("something went wrong");
        });
    }


    function getParameters(datasetName) {
        let url = '/getGraphFields/';
        let fd = new FormData();
        fd.append("dName", datasetName);
        $http.post(url, fd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            $scope.parametersArr = data;
            console.log("fieldsAr", $scope.parametersArr);

            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }


    $scope.createGraph = function () {
        console.log("in createGraph");
        let formd = new FormData();
        let val = document.getElementById('x_val');
        let v = val.options[val.selectedIndex].value;
        let graphDataUrl = '/getGraphData/';
        formd.append("x_value", v);
        val = document.getElementById('y_val');
        v = val.options[val.selectedIndex].value;
        formd.append("y_value", v);
        formd.append("dtName", datasetName);

        $http.post(graphDataUrl, formd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            xdata = data.labels;
            ydata = data.defaultData;
            divId = document.getElementById("chartEdit");
            viewChart(xdata, ydata, divId.id);
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    }


    $scope.delVisualization = function (visualizationId) {
        let url = '/delVisualization/' + visualizationId + '/';
        $http.delete(url)
            .success(function (data, status, headers) {
                console.log("in delete visualization http", data);
                if (data === 'delete successful') {
                    location.reload();
                }
                else {
                    alert("Visualization is not deleted successfully");
                }

            })
            .error(function (data, status, header, config) {
                console.log("something went wrong");
            });

    }

    $scope.updateVisualization = function () {
        console.log("graph data x", xData);
        console.log("graph data y", yData);
        let graphData = {
            "labels": xData,
            "defaultData": yData
        };
        //	console.log("this is from update vis",vId);
        let vUrl = '/updateVisualization/';
        let dt = new FormData();
        dt.append("visualization_name", $scope.visualName);
        dt.append("visualization_id", currChartid);
        dt.append("data", JSON.stringify(graphData));

        $http.post(vUrl, dt, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            if (data == "saved successfully") {
                alert("visualization is updated successfully");
            }
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }

});

module.controller("datasetListCtrl", function ($scope, $http) {
    $scope.test = "This is working datasetListCtrl";
    $scope.datasetArr = [];
//	$scope.viewClicked = false;
//	$scope.editClicked = false;
    console.log("datasetArr", $scope.datasetArr.length);
    let url = '/getDataset/'
    let x = [];
    $http.get(url)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.datasetArr = response.data;
            x = response.data[0].data;
            console.log("sdf", x);
            $scope.lenDatasetArr = $scope.datasetArr.length;
        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    $scope.viewDataset = function (dname, stringData) {
        let rowWiseData = stringData.split("\n");
        let h = rowWiseData[0].split(",");

        let table = "<table class='table table-bordered table-striped my-4'>";
        table += "<tr>";
        for (let k = 0; k < h.length; k++) {
            table += "<td class='head-color'>";
            table += h[k];
            table += "</td>";
        }
        table += "</tr>";


        for (let i = 1; i < rowWiseData.length; i++) {
            let rowDt = rowWiseData[i].split(",");
            table += "<tr>";
            for (let q = 0; q < rowDt.length; q++) {
                table += "<td>";
                table += rowDt[q];
                table += "</td>";
            }
            table += "</tr>";
        }
        table += "</table>";
        let modalLabel = 'Dataset :' + dname;
        $('#viewModalLabel').html(modalLabel);
        $('#viewModalBody').html(table);
    }

    $scope.delDataset = function (datasetName) {
        let datasetTodel = datasetName;
        let url = '/delete/' + datasetTodel + '/';
        console.log("url", url);
        $http.delete(url)
            .success(function (data, status, headers) {
                console.log("in delete data http", data);
                location.reload();
            })
            .error(function (data, status, header, config) {
                console.log("something went wrong");
            });

    };
});

module.controller("visualizationCtrl", function ($scope, $http) {
    $scope.test = "This is working visualizationCtrl";
    $scope.datasetArr = [];
    $scope.showGraph = false;
    $scope.showGraphList = false;
    $scope.fieldsAr = [];
    $scope.vName = '';
    let defaultData = [];
    let labels = [];
    let graphType = '';
    let selDatasetId = '';
    $scope.names = ["Emil", "Tobias", "Linus"];
    let url = '/getDataset/'
    $http.get(url)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.datasetArr = response.data;
        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });
    $scope.reload = function () {
        $scope.showGraph = false;
        $scope.showGraphList = false;
        location.reload();

    }

    function setChart() {
        //   var ctx = document.getElementById("myChart");
        var ctx2 = document.getElementById("myChart2");
        var myChart = new Chart(ctx2, {
//		type: 'pie',
            type: graphType,
            data: {
                labels: labels,
                datasets: [{
                    label: '',
                    data: defaultData,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {}
        });

        /*   var myChart = new Chart(ctx, {
         type: 'polarArea',
         data: {
         labels: labels,
         datasets: [{
         label: '# of Votes',
         data: defaultData,
         backgroundColor: [
         'rgba(255, 99, 132, 0.2)',
         'rgba(54, 162, 235, 0.2)',
         'rgba(255, 206, 86, 0.2)',
         'rgba(75, 192, 192, 0.2)',
         'rgba(153, 102, 255, 0.2)',
         'rgba(255, 159, 64, 0.2)'
         ],
         borderColor: [
         'rgba(255,99,132,1)',
         'rgba(54, 162, 235, 1)',
         'rgba(255, 206, 86, 1)',
         'rgba(75, 192, 192, 1)',
         'rgba(153, 102, 255, 1)',
         'rgba(255, 159, 64, 1)'
         ],
         borderWidth: 1
         }]
         },
         options: {
         scales: {
         yAxes: [{
         ticks: {
         beginAtZero:true
         }
         }]
         }
         }
         });*/
    }

    $scope.makeGraph = function () {
        console.log("in makeGraph");
        let formd = new FormData();
        let val = document.getElementById('x_value');
        let v = val.options[val.selectedIndex].value;
        let graphDataUrl = '/getGraphData/';
        formd.append("x_value", v);
        val = document.getElementById('y_value');
        v = val.options[val.selectedIndex].value;
        formd.append("y_value", v);
        formd.append("dtName", $scope.selectedDataset);
        console.log("data to send", formd);


        $http.post(graphDataUrl, formd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("graph data :", data);
            labels = data.labels
            defaultData = data.defaultData;
            setChart();
            console.log("graphtype", graphType);
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    }

    $scope.makeVisualization = function (dataset) {
        console.log("datasetName", dataset);
        selDatasetId = dataset.dataset_id;
        console.log("adsetid", selDatasetId);
        $scope.selectedDataset = dataset.dataset_name;
        let data = new FormData();
        let url = '/getGraphFields/';
        data.append("dName", dataset.dataset_name);

        $http.post(url, data, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            $scope.fieldsAr = data;
            console.log("fieldsAr", $scope.fieldsAr);
            $scope.showGraphList = true;
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }

    $scope.setGraphType = function (type) {
        graphType = type;
        console.log("grs", type);
        console.log("grs1", graphType);
        $scope.showGraph = true;
        $scope.showGraphList = false;
    }

    $scope.paramterSave = function () {
        let graphData = {
            "labels": labels,
            "defaultData": defaultData
        };
        let vUrl = '/saveGraph/';
        let dt = new FormData();
        dt.append("visualization_name", $scope.vName);
        dt.append("data", JSON.stringify(graphData));
        dt.append("dataset_id", selDatasetId);
        dt.append("graphType", graphType);
        console.log('graphy', graphData);

        $http.post(vUrl, dt, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("this is repsonse data", status);
            console.log("data is ", data);
            if (data == "saved successfully") {
                $('#successModal').modal();
            }
            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            console.log("something went wrong");

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });


    }


});
module.controller("processCtrl", function ($scope, $http, $route) {
    let currProcess = {};
    let prevProcess = {};
    let x = [];
    $scope.test = "This is working test3";
    $scope.processName = "";
    $scope.currentSelectedProcess = 'root';
    $scope.emptyProcess = false;
    $scope.onlyProcess = false;
    $scope.bothProcessDataset = false;
    $scope.createSuccess = false;
    $scope.dArr = [];
    $scope.pArr = [];
    $scope.parentProcessName = '';
    let response = [];
    let pform = new FormData();
    let processUrl = '/getProcessList/';
    let proUrl = '/getProcess/';
    pform.append("parent_process", 'PID' + $scope.currentSelectedProcess + '00000000000000');
    $http.post(processUrl, pform, {
        headers: {'Content-Type': undefined},
        transformRequest: angular.identity
    }).success(function (data, status, headers, config) {
        console.log("success", data);
        response = data;
        showPND();
        console.log("response", response);
        console.log("this is repsonse status", status);
    }).error(function (data, status, headers, config) {
        console.log("error occured");
    });

    $http.get(proUrl)
        .then(function (response) {
            //First function handles success
            console.log("get response", response);
            $scope.processAr = response.data;
            //	$scope.datasetArr = response.data;
        }, function (response) {
            //Second function handles error
            console.log("Something went wrong");
        });

    function showPND() {
        $scope.emptyProcess = false;
        $scope.onlyProcess = false;
        $scope.bothProcessDataset = false;
        if (response.length == 2) {
            $scope.dArr = response[1];
            $scope.pArr = response[0];
            if ($scope.dArr.length > 0) {
                $scope.bothProcessDataset = true;
            }
            if ($scope.pArr.length > 0) {
                $scope.onlyProcess = true;
            }
            console.log("processArr", $scope.pArr);
            console.log("dArr", $scope.dArr);
            if (($scope.dArr.length == 0) && ($scope.pArr.length == 0)) {
                $scope.emptyProcess = true;
                $scope.onlyProcess = false;
                $scope.bothProcessDataset = false;
            }
        }


    }

    $scope.createAnother = function () {
        $scope.createSuccess = false;
        $scope.processName = "";
    }
    $(document).ready(function () {
        $("#PIDthanos20180413090126").click(function () {
            alert("The paragraph was clicked.");
            console.log("sfdsfsdf", $(this).val());
            //	alert("dfgsdfg",$(this).text());

        });

        //	$('span').click(function(){
        //		var t = $(this).text();
        //		alert(t);
        //	});
    });


    $scope.backBtn = function () {
        let p_id = '';
        $scope.currentSelectedProcess = prevProcess.process_name;

        //	p_id = 'root'
        currProcess = prevProcess;
        p_id = currProcess.process_id;
        let f = new FormData();
        f.append("parent_process", p_id);
        console.log("current process", $scope.currentSelectedProcess);
        $http.post(processUrl, f, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("success");
            response = data;
            showPND();
            console.log("response", response);
            console.log("this is repsonse status", status);
        }).error(function (data, status, headers, config) {
            console.log("error occured");
        });

    }

    function getIndexNavBar(id) {
        console.log("lastPid", id);
        let i;
        let p = document.getElementById('process_nav').children;
        let x = document.getElementById('process_nav');
        console.log("children ", p);
        for (i = 0; i < p.length; i++) {
            if (id === p[i].attributes[1].value)
                break;
            //console.log("p[i].attributes[1]",p[i].attributes[1].value);
        }
        console.log("pIndex", i);
        //if(x.hasChildNodes()){
        //	x.removeChild(x.firstChild);
        //}
        return i;
    }

    function rmvFromNav(lastPid) {
        console.log("helooo");
        let index = getIndexNavBar(lastPid);
        let processNavBar = document.getElementById('process_nav').children;
        let x = document.getElementById('process_nav');
        let length = document.getElementById('process_nav').children.length;
        console.log("p len", length);
        index = index + 1;
        console.log("selected index", index);
        let k;
        //if(index != undefined){
        for (k = index; k <= length; k++) {
            //console.log("chilren",processNavBar[k]);
            x = document.getElementById('process_nav');
            x.removeChild(processNavBar[k]);
            console.log("removedchild", processNavBar[k]);

        }
        //}
    }

    $scope.rootProcess = function () {
        let pro = "PIDroot00000000000000";
        let xfm = new FormData();
        xfm.append("parent_process", pro);
        //	console.log("current process",$scope.currentSelectedProcess);
        $http.post(processUrl, xfm, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("success");
            response = data;
            showPND();
            console.log("response", response);
            console.log("this is repsonse status", status);
        }).error(function (data, status, headers, config) {
            console.log("error occured");
        });
        $scope.currentSelectedProcess = "root";
        rmvFromNav(pro);
    }

    $scope.selProcess = function (p) {
        console.log("p is ", p);
        currProcess = p;
        console.log("currProcess", currProcess);
        $scope.currentSelectedProcess = p.process_name;
        let x = document.createElement("span");
        let btn = document.createElement("p");
        let t = document.createTextNode(p.process_name);
        //	btn.setAttribute('href',"");
        //	x.setAttribute('ng-click',"selProcess(this)");
        x.setAttribute('class', " pointer breadcrumb-item active");
        x.setAttribute('id', p.process_id);
        x.setAttribute('name', p.process_name);
        x.setAttribute('value', p.process_id);
        //	x.setAttribute('onclick',"spanProcess()");
        //	x.innerHTML = p.process_name;
        //	x.appendChild(p);
        x.appendChild(t);
        let newTH = document.createElement('span');
        newTH.setAttribute('class', "breadcrumb-item active pointer");
        newTH.setAttribute('id', p.process_id);
        newTH.setAttribute('value', p.process_id);
        newTH.innerHTML = p.process_name;
        newTH.class = 'breadcrumb-item active';
        newTH.onclick = function () {
            console.log("sdfdsyahoo", this.id);
            //this.parentElement.removeChild(this);
            let navBarObj = {};
            let fm = new FormData();
            fm.append("parent_process", this.id);
            //	console.log("current process",$scope.currentSelectedProcess);
            $http.post(processUrl, fm, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                console.log("success");
                response = data;
                showPND();
                console.log("response", response);
                console.log("this is repsonse status", status);
            }).error(function (data, status, headers, config) {
                console.log("error occured");
            });
            if (this.id === 'root') {
                $scope.currentSelectedProcess = "root";
            }
            if (this.id !== 'root') {
                navBarObj.process_id = this.id;
                console.log("this much", this.innerHTML);
                navBarObj['process_name'] = this.innerHTML;
                navBarObj['process_id'] = this.id;
                currProcess = navBarObj;
            }
            rmvFromNav(this.id);

        };
        document.getElementById("process_nav").appendChild(newTH);
        let fm = new FormData();
        fm.append("parent_process", p.process_id);
        console.log("current process", $scope.currentSelectedProcess);
        $http.post(processUrl, fm, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("success");
            response = data;
            showPND();
            console.log("response", response);
            console.log("this is repsonse status", status);
        }).error(function (data, status, headers, config) {
            console.log("error occured");
        });

    }

      $scope.createProcess = function () {
        let process = $scope.processName;
        let url = '/makeProcess/';
        let fd = new FormData();
        console.log("this is process name");
        console.log(process);
        fd.append("process_name", process);
        if ($scope.currentSelectedProcess == 'root') {
            fd.append("parent_process", 'PID' + $scope.currentSelectedProcess + '00000000000000');
            console.log("viv process", $scope.currentSelectedProcess);
        }
        if ($scope.parentProcessName != '') {
            fd.append("parent_process", $scope.parentProcessName);
            console.log("selected process", $scope.parentProcessName);
        }
        //else if($scope.currentSelectedProcess==''){
        //fd.append("parent_process", currProcess.process_id);
        //}
        else {
            fd.append("parent_process", currProcess.process_id);
            console.log("currProcess2", currProcess.process_id);
        }
        console.log("sdgsdgs", $scope.currentSelectedProcess);

        $http.post(url, fd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {
            console.log("success");
            getList();
            //$scope.update = function
            $scope.createSuccess = true;
            console.log("this is repsonse status", status);
            //location.reload();
        }).error(function (data, status, headers, config) {
            console.log("error occured");
        });

        function getList() {
            let fm = new FormData();

            if ($scope.currentSelectedProcess == 'root') {
                fm.append("parent_process", 'PID' + $scope.currentSelectedProcess + '00000000000000');
                console.log("viv process", $scope.currentSelectedProcess);
            }
            else {
                fm.append("parent_process", currProcess.process_id);
                console.log("currProcess2", currProcess.process_id);
            }
            //    fm.append("parent_process",$scope.currentSelectedProcess);
            console.log("current process", $scope.currentSelectedProcess);
            $http.post(processUrl, fm, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                console.log("success");
                response = data;
                $scope.processAr = data;
                showPND();
                console.log("response", response);
                console.log("this is repsonse status", status);
            }).error(function (data, status, headers, config) {
                console.log("error occured");
            });
        }


    }
});
module.controller("createNewDataset", function ($scope, $http) {
    $scope.test = "This is working test4";
    $scope.fileType = 'none';
    $scope.test10 = "avengers assemble";
    $scope.datasetName = '';
    $scope.selectedProcess = '';
    let xoutput = '';
    var columnCount = 0;
    let headerArr = [];
    let typesArr = [];
    $scope.isFileUploaded = false;
    $scope.myVar = false;
    $scope.datasetNm = '';
    $scope.datasetSaved = false;
    $scope.showNextBtn = false;
    $scope.fileSelected = false;

    $scope.submitFileType = function () {
        if ($scope.fileType == 'mysql') {
            $("#mysqlPopup").modal();


        }

        else if ($scope.fileType !== '') {
            $scope.fileSelected = true;
            let url = '/getProcess/';
            $http.get(url)
                .then(function (response) {
                    //First function handles success
                    console.log("get response", response);
                    $scope.processList = response.data;
                    //    $scope.datasetArr = response.data;
                }, function (response) {
                    //Second function handles error
                    console.log("Something went wrong");
                });
        }
    }
  $scope.submitsqlconnection = function () {
        let hd = new FormData();
            hd.append("dbUrl", $scope.dbUrl);
            hd.append("userName", $scope.userName);
            hd.append("password", $scope.password);
            hd.append("port", $scope.port);
            hd.append("dbName", $scope.dbName);
            hd.append("tbName", $scope.tbName);
            let purl = '/mysqlconnect/';
            $("#mysqlPopup").modal("hide");
            $scope.fileSelected = true;
            let url = '/getProcess/';
            $http.get(url)
                .then(function (response) {
                    //First function handles success
                    console.log("get response", response);
                    $scope.processList = response.data;
                    //  $scope.datasetArr = response.data;
                }, function (response) {
                    //Second function handles error
                    console.log("Something went wrong");
                });

            $http.post(purl, hd, {
                    headers: {'Content-Type': undefined},
                    transformRequest: angular.identity
                }).success(function (data, status, headers, config) {
                    console.log("this is repsonse data", status);
                    console.log("this is repsonse data", data);
                    let csvData = data.csv;
                    let types = data.types;
               //     headerArr = types.split('\n');
                    console.log('today types',headerArr);
                    makeTypesArr(types);
                    xoutput = csvData;
                    displayHTMLTable(csvData);
                    // this callback will be called asynchronously
                    // when the response is available
                }).error(function (data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                });
    }

    function makeTypesArr(types){
        let temp = types.split('\n');
        temp = temp.slice(1);
        let type;
        for(type=0;type<temp.length-1;type++){
            let x = temp[type].split(',');
            typesArr.push(x[1]);
        }
        console.log('final types list',typesArr);
    }

    $(document).ready(function () {


        // $('#files').on("change",function(e){
        //	e.preventDefault();
        //	$('#files').parse({
        //		config: {
        //			delimiter: " ",
        //			complete: displayHTMLTable,
        //		},
        //		before: function(file, inputElem)
        //		{
        //			console.log("Parsing file...", file);
        //		},
        //		error: function(err, file)
        //		{
        //			console.log("ERROR:", err, file);
        //		},
        //		complete: function()
        //		{
        //	console.log("Done with all files");
        //		}
        //	});
        //	displayHTMLTable(xoutput);
        //   });


    });
    $scope.changeHeaderName = function (id) {
        console.log("index is ", id);
    }

    function displayHTMLTable(xout) {
        console.log("this is from displayHTMLTable", xout);
        var data = xout.split("\n");
        console.log("preview data", data);
        console.log("data is", data);
        var head = '';
        var head = data[0].split(",");
        headerArr = data[0].split(",");
        columnCount = head.length;
        var table = "<table class='table my-4'>";
        console.log("column count", columnCount);
        console.log("sdafad", head);


        for (i = 0; i < 1; i++) {
            table += "<tr class='head-color'>";
            for (j = 0; j < head.length; j++) {
                table += "<th>";
                table += "<input type='text' class='form-control' id='headerName" + j + "' placeholder='" + head[j] + "'>";
                table += "</th>";
            }
            table += "</tr>";
        }

        for (i = 0; i < 16; i++) {

            table += "<tr>";
            var row = data[i];
            console.log("row data", row);
            var cells = row.split(",");
            for (j = 0; j < cells.length; j++) {
                table += "<td>";
                table += cells[j];
                table += "</td>";
            }
            table += "</tr>";
        }
        table += "</table>";
        $("#parsed_csv_list").html(table);
    }

    function chngHeaderDatatypeTable(responseData) {
        let htm = "<p>" + responseData['fileData'] + "</p>"
        let dataInRow = responseData['fileData'].split("\n");
        let dataTypeArray = responseData['typesArray'];
        console.log("this is types array", dataTypeArray);
        //	dataTypeTable(dataTypeArray);

        let table = "<table class='table my-4'>";

        table += "<tr>";
        for (let k = 0; k < dataTypeArray.length; k++) {
            table += "<td class='head-color'>";
            table += "<input type='text' class='form-control' placeholder='" + dataTypeArray[k] + "' disabled='true' id='headerType" + k + "'>";
            table += "</td>";
        }
        table += "</tr>";

        for (i = 0; i < 1; i++) {
            table += "<tr>";
            console.log("this is column count", columnCount);
            for (j = 0; j < columnCount; j++) {
                console.log("this is column count", columnCount);
                table += "<td class='head-color'>";
                table += "<select id='header" + j + "' class='form-control custom-select btn-info'>" +
                    "<option selected>Data Type</option>" +
                    "<option value='String'>String</option>" +
                    "<option value='Integer'>Integer</option>" +
                    "<option value='Date'>Date</option>" +
                    "<option value='Decimal'>Decimal</option>" +
                    "</select>";
                table += "</td>";
            }
            table += "</tr>";
        }


        for (i = 0; i < 16; i++) {
            table += "<tr>";
            var row = dataInRow[i];
            var cells = row.split(",");
            for (j = 0; j < cells.length; j++) {
                table += "<td>";
                table += cells[j];
                table += "</td>";
            }
            table += "</tr>";
        }
        table += "</table>";
        $('#changeDataTypeDiv').html(table);

    }

    $scope.submitHeaderType = function () {
        let changedHeaderType = [];
        let headerObj = {};
        let successSaved = false;
        console.log("headertype array:", changedHeaderType);
        for (z = 0; z < columnCount; z++) {
            let p = document.getElementById('header' + z);
            let ev = p.options[p.selectedIndex].value;
            changedHeaderType[z] = ev;
        }
        for (q = 0; q < columnCount; q++) {
            if (changedHeaderType[q] != "Data Type") {
                headerObj[headerArr[q]] = changedHeaderType[q];
            }
        }
        console.log("headerObj", headerObj);
        let hd = new FormData();
        let ob = JSON.stringify(headerObj);
        console.log("yyyyy", ob);
        hd.append("changedDataType", ob);
        hd.append("dname", $scope.datasetName);
        console.log("dname", $scope.datasetName);
        console.log("hd", hd);
        let purl = '/upload/dataType/';
        console.log("formdata key", hd.keys());
        hdLen = Object.keys(headerObj).length;
        console.log("hd", hd);
        console.log("data to send", hd);
        if (hdLen != 0) {
            $http.post(purl, hd, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                console.log("this is repsonse data", status);
                successSaved = true;
                $scope.datasetSaved = true;
                $scope.fileSelected = false;
              //  $scope.fileSelected = false;
                // this callback will be called asynchronously
                // when the response is available
            }).error(function (data, status, headers, config) {
                successSaved = false;
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
        }
        else
            successSaved = true;

        if (successSaved) {
            $scope.datasetSaved = true;
            $scope.fileSelected = false;
        }
    }

    $scope.submit = function () {
        var changedHeaderName = [];
        console.log("head array is", headerArr);
        for (var i = 0; i < columnCount; i++) {
            console.log("i is ", i);
            var e = document.getElementById('headerName' + i).value;
            //	var hd = e.options[e.selectedIndex].value;
            console.log("hi", e);
            changedHeaderName[i] = e;
        }
        for (var v = 0; v < columnCount; v++) {
            if (changedHeaderName[v] != "") {
                headerArr[v] = changedHeaderName[v];
            }
        }

        console.log("head array is", headerArr);
        console.log("changed head array is", changedHeaderName);
        var fd = new FormData();
        datas = $("#upForm").serializeArray();
        // send other data in the form
        for (var i = 0; i < datas.length; i++) {
            fd.append(datas[i].name, datas[i].value);
        }
        // append file to FormData
        console.log("headers array", headerArr);
        fd.append("myfile", $("#files")[0].files[0]);
        fd.append("headers", headerArr);
        fd.append("allData", xoutput);
        fd.append("fileType", $scope.fileType);
        fd.append("process_id", $scope.selectedProcess);
        if($scope.fileType === 'mysql'){
            fd.append('types',typesArr);
        }
        console.log("select process", $scope.selectedProcess);
//	fd.append("headersDatatype",dataType);
        // for sending manual values
        //   fd.append("type", "edit");
//	console.log("df",fd);
        var durl = "/upload/";
        $http.post(durl, fd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {

            console.log("this is repsonse wala data", data);

            if (data.isDuplicate===true) {
                //data = 'Duplicate Dataset';
                confirm('Duplicate Dataset')
                location.reload();
                //alert("Change Dataset Name - A dataset name with same and process has already been created.");

            }
            else {
                $scope.isFileUploaded = true;
                $scope.myVar = true;
                chngHeaderDatatypeTable(data);
            }
            //	console.log("$scope.isFileUploaded",$scope.isFileUploaded);
            //console.log("data",data);

            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            $scope.isFileUploaded = false;

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }

    $scope.newDataset = function () {
        $scope.fileSelected = false;
        $http.get("#//createDataset")
            .then(function (response) {
                $scope.myWelcome = response.data;
                location.reload();
            });
    }

    //For excel support --- js-xls

    var X = XLSX;
    var XW = {
        /* worker message */
        msg: 'xlsx',
        /* worker scripts */
        worker: './xlsxworker.js'
    };

    var global_wb;

    var process_wb = (function () {
        var OUT = document.getElementById('out');
        var HTMLOUT = document.getElementById('htmlout');

        var get_format = (function () {
            var radios = document.getElementsByName("format");
            return function () {
                for (var i = 0; i < radios.length; ++i) if (radios[i].checked || radios.length === 1) return radios[i].value;
            };
        })();

        var to_json = function to_json(workbook) {
            var result = {};
            workbook.SheetNames.forEach(function (sheetName) {
                var roa = X.utils.sheet_to_json(workbook.Sheets[sheetName], {header: 1});
                if (roa.length) result[sheetName] = roa;
            });
            return JSON.stringify(result, 2, 2);
        };

        var to_csv = function to_csv(workbook) {
            var result = [];
            workbook.SheetNames.forEach(function (sheetName) {
                var csv = X.utils.sheet_to_csv(workbook.Sheets[sheetName]);
                console.log("from to csv", csv);
                if (csv.length) {
                    //	result.push("SHEET: " + sheetName);
                    //	result.push("");
                    result.push(csv);
                }
            });
            //	console.log("old result",result);
            //console.log("new result", result.join("\n"))
            return result.join("\n");
        };

        var to_fmla = function to_fmla(workbook) {
            var result = [];
            workbook.SheetNames.forEach(function (sheetName) {
                var formulae = X.utils.get_formulae(workbook.Sheets[sheetName]);
                if (formulae.length) {
                    result.push("SHEET: " + sheetName);
                    result.push("");
                    result.push(formulae.join("\n"));
                }
            });
            return result.join("\n");
        };

        var to_html = function to_html(workbook) {
            HTMLOUT.innerHTML = "";
            workbook.SheetNames.forEach(function (sheetName) {
                var htmlstr = X.write(workbook, {sheet: sheetName, type: 'string', bookType: 'html'});
                HTMLOUT.innerHTML += htmlstr;
            });
            return "";
        };

        return function process_wb(wb) {
            global_wb = wb;
            var output = "";
            switch (get_format()) {
                case "form":
                    output = to_fmla(wb);
                    break;
                case "html":
                    output = to_html(wb);
                    break;
                case "json":
                    output = to_json(wb);
                    break;
                default:
                    output = to_csv(wb);
            }
            console.log("this is my output", output);
            xoutput = output;
            console.log("this is xoutput", xoutput);
            displayHTMLTable(xoutput);
            //	if(OUT.innerText === undefined) OUT.textContent = output;
            //	else OUT.innerText = output;
            if (typeof console !== 'undefined') console.log("output", new Date());
        };
    })();

    var setfmt = window.setfmt = function setfmt() {
        if (global_wb) process_wb(global_wb);
    };

    var b64it = window.b64it = (function () {
        var tarea = document.getElementById('b64data');
        return function b64it() {
            if (typeof console !== 'undefined') console.log("onload", new Date());
            var wb = X.read(tarea.value, {type: 'base64', WTF: false});
            process_wb(wb);
        };
    })();

    var do_file = (function () {
        var rABS = typeof FileReader !== "undefined" && (FileReader.prototype || {}).readAsBinaryString;
        var domrabs = document.getElementsByName("userabs")[0];
        if (!rABS) domrabs.disabled = !(domrabs.checked = false);

        var use_worker = typeof Worker !== 'undefined';
        var domwork = document.getElementsByName("useworker")[0];
        if (!use_worker) domwork.disabled = !(domwork.checked = false);

        var xw = function xw(data, cb) {
            var worker = new Worker(XW.worker);
            worker.onmessage = function (e) {
                switch (e.data.t) {
                    case 'ready':
                        break;
                    case 'e':
                        console.error(e.data.d);
                        break;
                    case XW.msg:
                        cb(JSON.parse(e.data.d));
                        break;
                }
            };
            worker.postMessage({d: data, b: rABS ? 'binary' : 'array'});
        };

        return function do_file(files) {
            rABS = domrabs.checked;
            use_worker = domwork.checked;
            var f = files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                if (typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
                var data = e.target.result;
                if (!rABS) data = new Uint8Array(data);
                if (use_worker) xw(data, process_wb);
                else process_wb(X.read(data, {type: rABS ? 'binary' : 'array'}));
            };
            if (rABS) reader.readAsBinaryString(f);
            else reader.readAsArrayBuffer(f);
        };
    })();

    (function () {
        var drop = document.getElementById('drop');
        if (!drop.addEventListener) return;

        function handleDrop(e) {
            e.stopPropagation();
            e.preventDefault();
            do_file(e.dataTransfer.files);
            var dropInInput = document.getElementById('files');
            dropInInput.files = e.dataTransfer.files;
        }

        function handleDragover(e) {
            e.stopPropagation();
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        }

        drop.addEventListener('dragenter', handleDragover, false);
        drop.addEventListener('dragover', handleDragover, false);
        drop.addEventListener('drop', handleDrop, false);
    })();

    (function () {
        var files = document.getElementById('files');
        if (!files.addEventListener) return;
        function handleFile(e) {
            do_file(e.target.files);
        }

        files.addEventListener('change', handleFile, false);
    })();


});
module.controller("RouteController5", function ($scope, $http) {
    $scope.test10 = "avengers assemble";
    $scope.datasetName = '';
    let xoutput = '';
    var columnCount = 0;
    var headerArr = [];
    $scope.isFileUploaded = false;
    $scope.myVar = false;
    $scope.datasetNm = '';
    $scope.datasetSaved = false;
    $scope.showNextBtn = false;

    $(document).ready(function () {


        // $('#files').on("change",function(e){
        //	e.preventDefault();
        //	$('#files').parse({
        //		config: {
        //			delimiter: " ",
        //			complete: displayHTMLTable,
        //		},
        //		before: function(file, inputElem)
        //		{
        //			console.log("Parsing file...", file);
        //		},
        //		error: function(err, file)
        //		{
        //			console.log("ERROR:", err, file);
        //		},
        //		complete: function()
        //		{
        //	console.log("Done with all files");
        //		}
        //	});
        //	displayHTMLTable(xoutput);
        //   });


    });
    $scope.changeHeaderName = function (id) {
        console.log("index is ", id);
    }

    function displayHTMLTable(xout) {
        console.log("this is from displayHTMLTable", xout);
        var data = xout.split("\n");
        console.log("preview data", data);
        console.log("data is", data);
        var head = '';
        var head = data[0].split(",");
        headerArr = data[0].split(",");
        columnCount = head.length;
        var table = "<table class='table my-4'>";
        console.log("column count", columnCount);
        console.log("sdafad", head);


        for (i = 0; i < 1; i++) {
            table += "<tr class='head-color'>";
            for (j = 0; j < head.length; j++) {
                table += "<th>";
                table += "<input type='text' class='form-control' id='headerName" + j + "' placeholder='" + head[j] + "'>";
                table += "</th>";
            }
            table += "</tr>";
        }

        for (i = 0; i < 16; i++) {

            table += "<tr>";
            var row = data[i];
            console.log("row data", row);
            var cells = row.split(",");
            for (j = 0; j < cells.length; j++) {
                table += "<td>";
                table += cells[j];
                table += "</td>";
            }
            table += "</tr>";
        }
        table += "</table>";
        $("#parsed_csv_list").html(table);
    }

    function chngHeaderDatatypeTable(responseData) {
        let htm = "<p>" + responseData['fileData'] + "</p>"
        let dataInRow = responseData['fileData'].split("\n");
        let dataTypeArray = responseData['typesArray'];
        console.log("this is types array", dataTypeArray);
        //	dataTypeTable(dataTypeArray);

        let table = "<table class='table my-4'>";

        table += "<tr>";
        for (let k = 0; k < dataTypeArray.length; k++) {
            table += "<td class='head-color'>";
            table += "<input type='text' class='form-control' placeholder='" + dataTypeArray[k] + "' disabled='true' id='headerType" + k + "'>";
            table += "</td>";
        }
        table += "</tr>";

        for (i = 0; i < 1; i++) {
            table += "<tr>";
            console.log("this is column count", columnCount);
            for (j = 0; j < columnCount; j++) {
                console.log("this is column count", columnCount);
                table += "<td class='head-color'>";
                table += "<select id='header" + j + "' class='form-control custom-select btn-info'>" +
                    "<option selected>Data Type</option>" +
                    "<option value='String'>String</option>" +
                    "<option value='Integer'>Integer</option>" +
                    "<option value='Date'>Date</option>" +
                    "<option value='Decimal'>Decimal</option>" +
                    "</select>";
                table += "</td>";
            }
            table += "</tr>";
        }


        for (i = 0; i < 16; i++) {
            table += "<tr>";
            var row = dataInRow[i];
            var cells = row.split(",");
            for (j = 0; j < cells.length; j++) {
                table += "<td>";
                table += cells[j];
                table += "</td>";
            }
            table += "</tr>";
        }
        table += "</table>";
        $('#changeDataTypeDiv').html(table);

    }

    $scope.submitHeaderType = function () {
        let changedHeaderType = [];
        let headerObj = {};
        let successSaved = false;
        console.log("headertype array:", changedHeaderType);
        for (z = 0; z < columnCount; z++) {
            let p = document.getElementById('header' + z);
            let ev = p.options[p.selectedIndex].value;
            changedHeaderType[z] = ev;
        }
        for (q = 0; q < columnCount; q++) {
            if (changedHeaderType[q] != "Data Type") {
                headerObj[headerArr[q]] = changedHeaderType[q];
            }
        }
        console.log("headerObj", headerObj);
        let hd = new FormData();
        let ob = JSON.stringify(headerObj);
        console.log("yyyyy", ob);
        hd.append("changedDataType", ob);
        hd.append("dname", $scope.datasetName);
        console.log("dname", $scope.datasetName);
        console.log("hd", hd);
        let purl = '/upload/dataType/';
        console.log("formdata key", hd.keys());
        hdLen = Object.keys(headerObj).length;
        console.log("hd", hd);
        console.log("data to send", hd);
        if (hdLen != 0) {
            $http.post(purl, hd, {
                headers: {'Content-Type': undefined},
                transformRequest: angular.identity
            }).success(function (data, status, headers, config) {
                console.log("this is repsonse data", status);
                successSaved = true;
                $scope.datasetSaved = true;
                // this callback will be called asynchronously
                // when the response is available
            }).error(function (data, status, headers, config) {
                successSaved = false;
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
        }
        else
            successSaved = true;
        if (successSaved) {
            $scope.datasetSaved = true;
        }
    }

    $scope.submit = function () {
        var changedHeaderName = [];
        console.log("head array is", headerArr);
        for (var i = 0; i < columnCount; i++) {
            console.log("i is ", i);
            var e = document.getElementById('headerName' + i).value;
            //	var hd = e.options[e.selectedIndex].value;
            console.log("hi", e);
            changedHeaderName[i] = e;
        }
        for (var v = 0; v < columnCount; v++) {
            if (changedHeaderName[v] != "") {
                headerArr[v] = changedHeaderName[v];
            }
        }

        console.log("head array is", headerArr);
        console.log("changed head array is", changedHeaderName);
        var fd = new FormData();
        datas = $("#upForm").serializeArray();
        // send other data in the form
        for (var i = 0; i < datas.length; i++) {
            fd.append(datas[i].name, datas[i].value);
        }
        // append file to FormData
        fd.append("myfile", $("#files")[0].files[0]);
        fd.append("headers", headerArr);
        fd.append("allData", xoutput);
//	fd.append("headersDatatype",dataType);
        // for sending manual values
        //   fd.append("type", "edit");
//	console.log("df",fd);
        var durl = "/upload/";
        $http.post(durl, fd, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).success(function (data, status, headers, config) {

            console.log("this is repsonse wala data", data);
            if (confirm(data)) {
                data = 'Duplicate Dataset'
                location.relaod();
                //alert("Change Dataset Name - This dataset name has already been taken.");
            }
            else {
                $scope.isFileUploaded = true;
                $scope.myVar = true;
                chngHeaderDatatypeTable(data);
            }


            //	console.log("$scope.isFileUploaded",$scope.isFileUploaded);
            //console.log("data",data);

            // this callback will be called asynchronously
            // when the response is available
        }).error(function (data, status, headers, config) {
            $scope.isFileUploaded = false;

            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });

    }

    //For excel support --- js-xls

    var X = XLSX;
    var XW = {
        /* worker message */
        msg: 'xlsx',
        /* worker scripts */
        worker: './xlsxworker.js'
    };

    var global_wb;

    var process_wb = (function () {
        var OUT = document.getElementById('out');
        var HTMLOUT = document.getElementById('htmlout');

        var get_format = (function () {
            var radios = document.getElementsByName("format");
            return function () {
                for (var i = 0; i < radios.length; ++i) if (radios[i].checked || radios.length === 1) return radios[i].value;
            };
        })();

        var to_json = function to_json(workbook) {
            var result = {};
            workbook.SheetNames.forEach(function (sheetName) {
                var roa = X.utils.sheet_to_json(workbook.Sheets[sheetName], {header: 1});
                if (roa.length) result[sheetName] = roa;
            });
            return JSON.stringify(result, 2, 2);
        };

        var to_csv = function to_csv(workbook) {
            var result = [];
            workbook.SheetNames.forEach(function (sheetName) {
                var csv = X.utils.sheet_to_csv(workbook.Sheets[sheetName]);
                console.log("from to csv", csv);
                if (csv.length) {
                    //	result.push("SHEET: " + sheetName);
                    //	result.push("");
                    result.push(csv);
                }
            });
            //	console.log("old result",result);
            //console.log("new result", result.join("\n"))
            return result.join("\n");
        };

        var to_fmla = function to_fmla(workbook) {
            var result = [];
            workbook.SheetNames.forEach(function (sheetName) {
                var formulae = X.utils.get_formulae(workbook.Sheets[sheetName]);
                if (formulae.length) {
                    result.push("SHEET: " + sheetName);
                    result.push("");
                    result.push(formulae.join("\n"));
                }
            });
            return result.join("\n");
        };

        var to_html = function to_html(workbook) {
            HTMLOUT.innerHTML = "";
            workbook.SheetNames.forEach(function (sheetName) {
                var htmlstr = X.write(workbook, {sheet: sheetName, type: 'string', bookType: 'html'});
                HTMLOUT.innerHTML += htmlstr;
            });
            return "";
        };

        return function process_wb(wb) {
            global_wb = wb;
            var output = "";
            switch (get_format()) {
                case "form":
                    output = to_fmla(wb);
                    break;
                case "html":
                    output = to_html(wb);
                    break;
                case "json":
                    output = to_json(wb);
                    break;
                default:
                    output = to_csv(wb);
            }
            console.log("this is my output", output);
            xoutput = output;
            console.log("this is xoutput", xoutput);
            displayHTMLTable(xoutput);
            //	if(OUT.innerText === undefined) OUT.textContent = output;
            //	else OUT.innerText = output;
            if (typeof console !== 'undefined') console.log("output", new Date());
        };
    })();

    var setfmt = window.setfmt = function setfmt() {
        if (global_wb) process_wb(global_wb);
    };

    var b64it = window.b64it = (function () {
        var tarea = document.getElementById('b64data');
        return function b64it() {
            if (typeof console !== 'undefined') console.log("onload", new Date());
            var wb = X.read(tarea.value, {type: 'base64', WTF: false});
            process_wb(wb);
        };
    })();

    var do_file = (function () {
        var rABS = typeof FileReader !== "undefined" && (FileReader.prototype || {}).readAsBinaryString;
        var domrabs = document.getElementsByName("userabs")[0];
        if (!rABS) domrabs.disabled = !(domrabs.checked = false);

        var use_worker = typeof Worker !== 'undefined';
        var domwork = document.getElementsByName("useworker")[0];
        if (!use_worker) domwork.disabled = !(domwork.checked = false);

        var xw = function xw(data, cb) {
            var worker = new Worker(XW.worker);
            worker.onmessage = function (e) {
                switch (e.data.t) {
                    case 'ready':
                        break;
                    case 'e':
                        console.error(e.data.d);
                        break;
                    case XW.msg:
                        cb(JSON.parse(e.data.d));
                        break;
                }
            };
            worker.postMessage({d: data, b: rABS ? 'binary' : 'array'});
        };

        return function do_file(files) {
            rABS = domrabs.checked;
            use_worker = domwork.checked;
            var f = files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                if (typeof console !== 'undefined') console.log("onload", new Date(), rABS, use_worker);
                var data = e.target.result;
                if (!rABS) data = new Uint8Array(data);
                if (use_worker) xw(data, process_wb);
                else process_wb(X.read(data, {type: rABS ? 'binary' : 'array'}));
            };
            if (rABS) reader.readAsBinaryString(f);
            else reader.readAsArrayBuffer(f);
        };
    })();

    (function () {
        var drop = document.getElementById('drop');
        if (!drop.addEventListener) return;

        function handleDrop(e) {
            e.stopPropagation();
            e.preventDefault();
            do_file(e.dataTransfer.files);
        }

        function handleDragover(e) {
            e.stopPropagation();
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        }

        drop.addEventListener('dragenter', handleDragover, false);
        drop.addEventListener('dragover', handleDragover, false);
        drop.addEventListener('drop', handleDrop, false);
    })();

    (function () {
        var files = document.getElementById('files');
        if (!files.addEventListener) return;
        function handleFile(e) {
            do_file(e.target.files);
        }

        files.addEventListener('change', handleFile, false);
    })();


});
module.controller('MainCtrl', function ($scope) {
    $scope.title = 'Read CSV file with Angular';
});

module.directive('fileReader', function () {
    return {
        scope: {
            fileReader: "="
        },
        link: function (scope, element) {
            $(element).on('change', function (changeEvent) {
                var files = changeEvent.target.files;
                if (files.length) {
                    var r = new FileReader();
                    r.onload = function (e) {
                        var contents = e.target.result;
                        scope.$apply(function () {
                            scope.fileReader = contents;
                            scope.testing = contents;
                        });
                    };

                    r.readAsText(files[0]);
                }
            });
        }
    };
});
