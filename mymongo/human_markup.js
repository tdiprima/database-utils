// RUN LOCALLY
db.tumor_annotations.find().forEach(function(data) {
    //print(data.provenance.image.case_id.replace("VTRPDAC_Test_", ""))
    db.tumor_annotations.update({
        "_id": data._id
    }, {
        "$set": {
            "provenance.image.imageid": data.provenance.image.case_id.replace("VTRPDAC_Test_", ""),
            "provenance.image.study": data.provenance.image.case_id.replace("VTRPDAC_Test_", ""),
            "provenance.image.subject": data.provenance.image.case_id.replace("VTRPDAC_Test_", "")
        }
    });
    
})
