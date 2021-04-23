@outputSchema('wikidatauri:chararray')
def convert_wikidatauri(the_input):
    # This converts bag of tuples into first tuple's string
    lOut = the_input[0];
    lOut = lOut[0];
    #lOut = str(type(lOut));
    #for i,l in enumerate(the_input):
    #    lNew = [i,] + l
    #    lOut.append(lNew)
    return lOut

@outputSchema('name:chararray')
def convert_name(the_input):
    # This converts bag of tuples into first tuple's string
    lOut = the_input[0];
    lOut = lOut[0];
    #lOut = str(type(lOut));
    #for i,l in enumerate(the_input):
    #    lNew = [i,] + l
    #    lOut.append(lNew)
    return lOut
    
@outputSchema('label:chararray')
def convert_label(the_input):
    # This converts bag of tuples into first tuple's string
    lOut = the_input[0];
    lOut = lOut[0];
    return lOut

    
@outputSchema('timeinterval:chararray')
def convert_date(the_input):
    lOut = the_input;
    output = "";
    set(lOut);
    lOut.sort();
    if (len(lOut) > 1):
        lOut=(lOut[0], lOut[-1]);
    for var in lOut:
        varvalue = var[0];
        varvalue = varvalue[:4];
        if (lOut.index(var) == 0):
            output = '<['+varvalue;
            if (len(lOut) == 1):
            	output = output + ', ' + varvalue + ']'; 
        else:
            output = output + ', ' + varvalue;
    if (len(lOut) != 1):
        output = output + ']'; 
    output = output + '>\"';
    return output
    
@outputSchema('timestamp:chararray')
def convert_date_edge(the_input):
    # This converts bag of tuples into first tuple's string
    lOut = the_input[0];
    item = lOut[0];
    lOut = '<['+item[:4]+', '+item[:4]+ ']>\"';
    return lOut
    
@outputSchema('timeintervalr:chararray')
def convert_date_r(the_input):
    lOut = the_input;
    output = "";
    set(lOut);
    lOut.sort();
    if (len(lOut) > 1):
        lOut=(lOut[0], lOut[-1]);
    for var in lOut:
        varvalue = var[0];
    	varvalue = varvalue[:4];
        if (lOut.index(var) == 0):
            output = ' onset '+varvalue+'.0' + ' start '+varvalue;
            duration = float(varvalue+'.0');
            start = varvalue;
            if (len(lOut) == 1):
            	duration = float(varvalue+'.9')-duration;
            	output = output + ' terminus ' + varvalue+'.9' + ' end ' + varvalue +' duration '+str(duration); 
        else:
            output = ' onset ' + str(duration) + ' start ' + str(start) +' terminus ' + varvalue+'.9' + ' end ' + varvalue;
            duration = float(varvalue+'.9') - duration;
            output = output + ' duration '+str(duration);
            #output = output + ' terminus ' + varvalue+'.9' + ' duration '+str(duration);
    return output
    
@outputSchema('timestampr:chararray')
def convert_date_edge_r(the_input):
    # This converts bag of tuples into first tuple's string
    lOut = the_input[0];
    item = lOut[0];
    lOut = 'onset '+item[:4]+'.0 terminus '+item[:4]+'.9' + ' duration 0.9';
    return lOut
    
@outputSchema('timestampr:chararray')
def convert_date_merged_edge_r(the_input):
    years = [];
    lOut=the_input;
    output="";
    for var in lOut:
        varvalue=var[3];
        for varList in varvalue:
            varvalueList=varList[0];
            output = output + " | " + varvalueList;
            years.append(varvalueList);
    list(years);
    years.sort();
    if (len(years) > 1):
        #years=(years[0], years[-1]);
        outputStart=str(years[0]);
        outputOnset=outputStart+'.0';
        outputEnd=str(years[-1]);
        duration=int(years[-1])-int(years[0])+0.9;
        #onset 1977.0 start 1977 terminus 1977.9 end 1977 duration 0.9 
        output = 'onset ' + outputOnset + ' start ' + outputStart +' terminus ' + outputEnd+'.9' + ' end ' + outputEnd + ' duration ' + str(duration);
    #for var in years:
        #varvalue = var;
        #if (years.index(var) == 0):
        #    output = ' onset '+varvalue+'.0' + ' start '+varvalue;
        #    duration = float(varvalue+'.0');
        #    start = varvalue;
        #    if (len(years) == 1):
        #    	duration = float(varvalue+'.9')-duration;
        #    	output = output + ' terminus ' + varvalue+'.9' + ' end ' + varvalue +' duration '+str(duration); 
        #else:
        #output = ' onset ' + str(duration) + ' start ' + str(start) +' terminus ' + varvalue+'.9' + ' end ' + varvalue;
        #duration = float(varvalue+'.9') - duration;
        #output = output + ' duration '+str(duration);
        #output = output + ' terminus ' + varvalue+'.9' + ' duration '+str(duration);
    return output

@outputSchema('magazines:chararray')
def merged_edge_r_magazines(the_input):
    magazines = [];
    lOut=the_input;
    output="";
    for var in lOut:
        varvalue=var[1];
        start = varvalue.find('|')+1
        end = varvalue.find('...', start)
        output = output + "_" + varvalue[start:end];
        magazines.append(varvalue[start:end]);
    # insert the list to the set 
    list_set = set(magazines) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    unique_magazines = "";
    for x in unique_list: 
        unique_magazines=unique_magazines + "_" + x;
    #this returns unique list of magazines
    return unique_magazines
    #this would return all instances of magazine
    #return output;