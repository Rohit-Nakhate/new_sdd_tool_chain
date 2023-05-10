import os
import csv


# Relevant Requirements Filter:
allowed_maturity = ['project_accepted']
allowed_type = ['functional_requirement', 'nonfunctional_requirement']
allowed_variant = "ICAS1evo"


# SW Version as integer e.g. if ID.SW4.0_0152 -> 152
def get_req_ids(file_path, target_release):

    relevant_req = []
    future_rel_req = []
    invalid_from_req = []

    with open(file_path, "r", encoding='utf-8-sig') as csv_file:
        csvd = csv.DictReader(csv_file, delimiter=';')

        for line in csvd:
            # Prefilter Headings etc.
            if line["c_This_is_a"] in allowed_type and line["c_Maturity"] in allowed_maturity:
                # Filter variant
                if allowed_variant in line["c_Variant"].split("\n"):
                    # Check if for future release
                    if line["p_Release_ICAS1evo"]:
                        # valid from = größer than target -> not relevant
                        # valid from = < target -> relevant
                        # valid from = not prvided -> not relevvant
                        valid_from = line["p_Release_ICAS1evo"].split("_")
                        if len(valid_from) < 2: # e.g. ID.SW.5.0
                            future_rel_req.append(line["Object Identifier"])

                        if len(valid_from) >= 2: # e.g. ID.SW.5.0_0400
                            if int(valid_from[1]) > target_release:
                                future_rel_req.append(line["Object Identifier"])

                    # Check if invalid from provided
                    if line["p_ICAS1evo_invalid_from"] != "N/A":
                        if "IS" in line["p_ICAS1evo_invalid_from"]:
                            print("Error - Attribute: invalid_from - Expected format: ID.SW4.0_0134 - Current Value: " +
                              line["p_ICAS1evo_invalid_from"])
                        else:
                            invalid_from = line["p_ICAS1evo_invalid_from"].split("_")
                            if len(invalid_from) < 2:
                                print("Error - Attribute: invalid_from - No SW version provided. Expected format: ID.SW4.0_0134 - Current Value: "
                                      + line["p_ICAS1evo_invalid_from"])
                            else:
                                sw_version_invalid_from = int(invalid_from[1])
                                # target = 140, invalid from = 136 -> req not relevant
                                # target = 140, invalid from = 140 -> req not relevant
                                # target = 140, invalid from = 142 -> req is relvanent
                                if target_release < sw_version_invalid_from:
                                    relevant_req.append(line["Object Identifier"])
                    else:
                        relevant_req.append(line["Object Identifier"])

    # Check if future releases in relevant requirements
    for fut in future_rel_req:
        if fut in relevant_req:
            relevant_req.remove(fut)

    print(future_rel_req)
    # print(relevant_req)

    doors_req = {
        "relevant_req": relevant_req,
        "future_req": future_rel_req,
        "invalid_from_req": invalid_from_req
    }

    return doors_req



