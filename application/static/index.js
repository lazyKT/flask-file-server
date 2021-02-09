/** index.js */

(function() {

    const tag = (document.getElementById('tag').innerHTML).toLowerCase()

    switch(tag) {
        case 'cdm':
            tag.stye.background = 'red'
            break;
        case 'violence':
            tag.stye.background = 'green'
            break;
        case 'alert':
            tag.stye.background = "orange"
            break;
        default:
            tag.stye.background = 'black'
            break;
    }

})()


async function upload_desc (desc) {
    const tag = "CDM";
    try {
        const response = await fetch('/upload-desc', {
            method : 'POST',
            headers: {
                Accept: 'application/json',
                'Content-type' : 'application/json'
            },
            body : JSON.stringify({ desc, tag })
        });

        const data = await response.json();
        const status = response.status;

        console.log("Desc Response", data, status);

        if ( status === 201 )
            return data.msg.id;
        
        return null;
    }
    catch (e) {
        console.error(e);
    }
}


async function upload_file() {

    const file = document.getElementById("input").files[0];
    const description = document.getElementById("desc").value;
    const formData = new FormData();
    formData.append("file", file);

    try {

        const id = await upload_desc(description);
        // const { id } = data;
        console.log("id", id);
        if (id === null || id === '')
            return;

        const response = await fetch(`/upload/${id}`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        const status = response.status;

        console.log("Upload Response ", data, status);
        
        // refresh page
        window.location.reload();

    }
    catch (e) {
        console.error('Upload Error : ', e);
    }

    return false;
}