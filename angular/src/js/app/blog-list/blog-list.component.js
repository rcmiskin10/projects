'use-strict';

angular.module('blogList').
	component('blogList', {
		
		templateUrl: '/templates/blog-list.html',
		controller: function(Post, $routeParams, $rootScope, $location, $scope){
			$scope.goToItem = function(post){
				
				$rootScope.$apply(function(){
					$location.path("/blog/" + post.id )
				})
			}
			$scope.changeCols = function(number){
				if (angular.isNumber(number)){
					$scope.numCols = number
				}else{
					$scope.numCols = 2
				}

				setupCol($scope.items, $scope.numCols)
			}
			
			$scope.loadingQuery = false
			$scope.$watch(function(){
				console.log($scope.query)
				if($scope.query){
					$scope.loadingQuery = true
					$scope.cssClass = 'col-sm-12'
				}else{
					if($scope.loadingQuery){
						setupCol($scope.items, 2)
						$scope.loadingQuery = false
					}
					
				}
			})
			function setupCol(data, number){
				if (angular.isNumber(number)){
					$scope.numCols = number
				}else{
					$scope.numCols = 2
				}
				
				$scope.cssClass = 'col-sm-' +(12/$scope.numCols)
				$scope.items = data
				$scope.colItems = chunkArrayInGroups(data,$scope.numCols)
			}

			Post.query(function(data){
					setupCol(data, 4)
				}, function(errorData){

			});
			//in order to find out how many columns in array
			function chunkArrayInGroups(array,unit){
				var results = [],
				length = Math.ceil(array.length / unit);
				for (var i = 0; i<length; i++){
					results.push(array.slice(i*unit,(i+1)*unit));
				}
				return results;
			}


			}

	});
