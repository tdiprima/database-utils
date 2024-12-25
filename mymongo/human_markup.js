// Modifies each document in the tumor_annotations collection by reassigning the properties: imageid, study, and subject
// of the image object inside the provenance object, by replacing the "VTRPDAC_Test_" substring in the case_id property
// value with an empty string.
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
