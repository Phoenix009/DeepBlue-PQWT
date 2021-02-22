


  
const saveDepartmentOrderButton = document.getElementById("save-department-order");
  
  
async function updateDepartmentOrder(){
  
      departmentList = document.getElementById('department_list').children
      console.log(departmentList);
      departmentOrder = [];
      for(var i = 0; i < departmentList.length; i++){
          departmentObject = {
              order : i + 1,
              pk :parseInt(departmentList[i].id)
          }
          departmentOrder.push(departmentObject);
      }
      const serializedDepartmentOrder = JSON.stringify(departmentOrder);
      console.log(serializedDepartmentOrder);
      console.log(departmentOrder);
      await handleReorderDepartments(serializedDepartmentOrder);
      window.location.reload();
  }
  
  
  saveDepartmentOrderButton.addEventListener("click", updateDepartmentOrder);

handleReorderDepartments = (payload)=>{
    const URL = '/departments/reorder';
    const csrftoken = getToken('csrftoken'); 
    const config = {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        }, 
        body: payload,
    }
    fetch(URL,config)
    .then((response)=>response.json())
    .then((data)=>{
        console.log(data);
    });

}
