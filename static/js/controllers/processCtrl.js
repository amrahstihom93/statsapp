angular.module("statsApp", ['ngRoute','http']).controller("RouteController3", function($scope,$http) {
    $scope.test="This is working test3";
	$scope.processName = "";
	$scope.createProcess = function(){
		var process = $scope.processName;
		console.log("this is process name");
		console.log($scope.processName);
		$scope.processName = 'none';
		var frm = document.getElementById('createProcessForm');
		$http({
			method : "POST",
			url : "/signup_success/",
			data : createProcessForm
		}).then(function mySuccess(response) {
			$scope.myWelcome = response.data;
		}, function myError(response) {
			$scope.myWelcome = response.statusText;
		});
	}
});