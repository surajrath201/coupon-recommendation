
var app = angular.module('myApp', []);

app.controller('myController', function ($scope, $http) {
	var vm = $scope;
	vm.formData = {};
	vm.message = null;
	vm.chartData = null;
	vm.result = 0;
	vm.customerDetails = 1;

	vm.back = function () {
		vm.customerDetails = 1;
		vm.result = 0;
		vm.formData = {
			hasChildren: 0
		};
		vm.message = null;
		vm.chartData = {};
		vm.chartData2 = {};
		vm.resultList = null;
	}

	vm.formData = {
		hasChildren: 0
	};

	vm.submitForm = function () {
		$http({
			method: 'POST',
			url: 'http://127.0.0.1:5000/submit-form',
			data: vm.formData
		})
			.then(function (response) {
				console.log(response);
				vm.result = 1;
				vm.customerDetails = 0;
				vm.message = response.data.accepted;
				vm.chartData = { 'labels': response.data.labels, 'data': response.data.bar };
				vm.chartData2 = {'labels': response.data.couponType, 'data': response.data.couponCount};
				vm.resultList = response.data.result;
				vm.renderChart();
			}, function (error) {
				console.log(error);
				vm.message = 'An error occurred while sending the message.';
			});
	};



	vm.renderChart = function () {

		//chart 1 for acceptance out of total coupon
		var labels = vm.chartData.labels;
		var data = vm.chartData.data;

		var ctx = document.getElementById('myChart').getContext('2d');
		new Chart(ctx, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [{
					label: 'Acceptance Rate',
					data: data,
					backgroundColor: 'rgba(54, 162, 235, 0.5)',
					borderColor: 'rgba(54, 162, 235, 1)',
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

		//chart 2 for coupon of different type
		// Render chart 2
		var labels2 = vm.chartData2.labels;
		var data2 = vm.chartData2.data;
	
		var ctx2 = document.getElementById('myChart2').getContext('2d');

		new Chart(ctx2, {
			type: 'bar',
			data: {
				labels: labels2,
				datasets: [{
					label: 'Coupons Distribution',
					data: data2,
					backgroundColor: 'rgba(54, 162, 235, 0.5)',
					borderColor: 'rgba(54, 162, 235, 1)',
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});
	};
});
