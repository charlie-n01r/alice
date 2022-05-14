using JSON

try
    file = open("vm_input.json", "r");
    input = JSON.parse(read(file, String));
    close(file);

    constants = input["constants"];
    modules = input["modules"];
    instructions = input["code"];
    bmem = input["base memory"];
    input = nothing;
    value = nothing;
    IP = 1;

    while true
        current = instructions[IP];
        if current[1] == "EndProgram"
            break;
        elseif current[1] == "Goto"
            IP = current[4] + 1;
            continue;
        elseif current[1] == "Print"
            for constant ∈ constants
                if constant[2] != current[4]
                    continue;
                end
                if constant[2] >= 29000
                    value = constant[1][2:end-1];
                else
                    value = constant[1];
                end
            end
            if instructions[IP + 1][1] == "Print"
                print(value, " ");
                IP += 1;
                continue;
            else
                println(value);
                IP += 1;
                continue;
            end
        elseif current[1] == "Input"
            for constant ∈ constants
                if constant[2] != current[3]
                    continue;
                end
                value = constant[1][2:end-1];
            end
            print(value);
            IP += 1;
            continue;
        else
            println(current);
            IP += 1;
            continue;
        end
        break;
    end
catch
    exit()
end

#=
    1000
    3000
    5000
    ----
    6000
    8000
    10000
    -----
    11000
    16000
    21000
    -----
    26000
    27500
    29000
=#
