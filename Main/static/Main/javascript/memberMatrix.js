let matrix = {'Total':{'Male':0,'Female':0,'Others':0,'Total':0}};

function updateMatrix(attributeId = null, column = null, subjectId = null ) {
    
    if (attributeId!=null && column!=null && subjectId!=null)
    {
        value = $("#"+subjectId).val();
        matrix[attributeId][column] = (isNaN(value) || value=='') ? 0 : parseInt(value);
    }

    matrix['Total']={'Male':0,'Female':0,'Others':0,'Total':0};

    for (row in matrix) {
        let Total = matrix[row]['Male']+matrix[row]['Female']+matrix[row]['Others'];
        matrix[row]['Total'] = Total;
        $("#M-"+row+"-T").val(Total);
        
        if(matrix[row]['Operator']=='+')
        {
            matrix['Total']['Male']+=matrix[row]['Male'];
            matrix['Total']['Female']+=matrix[row]['Female'];
            matrix['Total']['Others']+=matrix[row]['Others'];
            matrix['Total']['Total']+=matrix[row]['Total'];
        }
        else if(matrix[row]['Operator']=='-')
        {
            matrix['Total']['Male']-=matrix[row]['Male'];
            matrix['Total']['Female']-=matrix[row]['Female'];
            matrix['Total']['Others']-=matrix[row]['Others'];
            matrix['Total']['Total']-=matrix[row]['Total'];
        }
    } 
    appendMemberMatrixTotalRow(matrix['Total']['Male'],matrix['Total']['Female'],matrix['Total']['Others'],matrix['Total']['Total']);
    countN = (1 in matrix) ? matrix[1]['Total'] : null ;
    countn = (2 in matrix) ? matrix[2]['Total'] : null ;
    
    updateTotalNumberOfMembers();
    updateTotalNumberOfInductedMembers();
    updateOwedMoney();
    updatePending();
    if (countn != null) $('#dues02').val(countn);
}

