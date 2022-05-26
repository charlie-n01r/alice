include("virtual_memory.jl")
using JSON, Printf

IP = 1
Fun = []
Global = GlobalMem(Persistent([], [], []), Persistent([], [], []))
CurrMem = MemoryObj(Persistent([], [], []), Temporary([], [], [], []))
MemoryStack = [CurrMem]
PointerStack = [IP]

function extract()
    try
        file = open("obj.json", "r")
        input = JSON.parse(read(file, String))
        close(file)
        input["constants"], input["modules"], input["code"]
    catch LoadError
        exit()
    end
end

function store_or_fetch(address::Int64, do_store::Bool, value::Any=false)
    if address ∈ ranges[1]
        do_store && return store(Global.variables, value, convert(UInt16, address - ranges[1][1] + 1), '1')
        return fetch(Global.variables, convert(UInt16, address - ranges[1][1] + 1), '1')
    elseif address ∈ ranges[2]
        do_store && return store(Global.variables, value, convert(UInt16, address - ranges[2][1] + 1), '2')
        return fetch(Global.variables, convert(UInt16, address - ranges[2][1] + 1), '2')
    elseif address ∈ ranges[3]
        do_store && return store(Global.variables, value, convert(UInt16, address - ranges[3][1] + 1), '3')
        return fetch(Global.variables, convert(UInt16, address - ranges[3][1] + 1), '3')
    elseif address ∈ ranges[4]
        do_store && return store(MemoryStack[end].persistent, value, convert(UInt16, address - ranges[4][1] + 1), '1')
        return fetch(MemoryStack[end].persistent, convert(UInt16, address - ranges[4][1] + 1), '1')
    elseif address ∈ ranges[5]
        do_store && return store(MemoryStack[end].persistent, value, convert(UInt16, address - ranges[5][1] + 1), '2')
        return fetch(MemoryStack[end].persistent, convert(UInt16, address - ranges[5][1] + 1), '2')
    elseif address ∈ ranges[6]
        do_store && return store(MemoryStack[end].persistent, value, convert(UInt16, address - ranges[6][1] + 1), '3')
        return fetch(MemoryStack[end].persistent, convert(UInt16, address - ranges[6][1] + 1), '3')
    elseif address ∈ ranges[7]
        do_store && return store(MemoryStack[end].temporary, value, convert(UInt16, address - ranges[7][1] + 1), '1')
        return fetch(MemoryStack[end].temporary, convert(UInt16, address - ranges[7][1] + 1), '1')
    elseif address ∈ ranges[8]
        do_store && return store(MemoryStack[end].temporary, value, convert(UInt16, address - ranges[8][1] + 1), '2')
        return fetch(MemoryStack[end].temporary, convert(UInt16, address - ranges[8][1] + 1), '2')
    elseif address ∈ ranges[9]
        do_store && return store(MemoryStack[end].temporary, value, convert(UInt16, address - ranges[9][1] + 1), '3')
        return fetch(MemoryStack[end].temporary, convert(UInt16, address - ranges[9][1] + 1), '3')
    elseif address ∈ ranges[10]
        do_store && return store(Global.constants, value, convert(UInt16, address - ranges[10][1] + 1), '1')
        return fetch(Global.constants, convert(UInt16, address - ranges[10][1] + 1), '1')
    elseif address ∈ ranges[11]
        do_store && return store(Global.constants, value, convert(UInt16, address - ranges[11][1] + 1), '2')
        return fetch(Global.constants, convert(UInt16, address - ranges[11][1] + 1), '2')
    elseif address ∈ ranges[12]
        do_store && return store(Global.constants, value, convert(UInt16, address - ranges[12][1] + 1), '3')
        fetch(Global.constants, convert(UInt16, address - ranges[12][1] + 1), '3')
    else
        do_store && return store(MemoryStack[end].temporary, value, convert(UInt16, address - ranges[13][1] + 1), '4')
        return fetch(MemoryStack[end].temporary, convert(UInt16, address - ranges[13][1] + 1), '4')
    end
end

function conversion(address::Int64, value::String)
    if address ∈ ranges[1] || address ∈ ranges[4] || address ∈ ranges[7] || address ∈ ranges[10]
        return parse(Int64, value)
    elseif address ∈ ranges[2] || address ∈ ranges[5] || address ∈ ranges[8] || address ∈ ranges[11]
        return parse(Float64, value)
    elseif address ∈ ranges[9]
        return parse(Bool, value)
    elseif address ∈ ranges[end]
        return parse(UInt16, value)
    else
        return value
    end
end

function operations(data::Vector{Any}, operation::String)
    left = data[2] == nothing ? 0 : store_or_fetch(data[2], false)
    right = store_or_fetch(data[3], false)
    # Arithmetic
    operation == "+" && store_or_fetch(data[4], true, left + right)
    operation == "-" && store_or_fetch(data[4], true, left - right)
    operation == "*" && store_or_fetch(data[4], true, left * right)
    try
        operation == "^" && store_or_fetch(data[4], true, left ^ right)
    catch DomainError
        println("Error! Expression returned imaginary result!")
        exit()
    end
    if operation == "/"
        result = left / right
        if result == Inf
            println("Error! Division by zero is undefined!")
            exit()
        end
        result = store_or_fetch(data[4], true, result)
    end
    operation == "++" && store_or_fetch(data[4], true, right + 1)
    operation == "--" && store_or_fetch(data[4], true, right - 1)
    # Boolean logic
    operation == ">" && store_or_fetch(data[4], true, left > right)
    operation == ">=" && store_or_fetch(data[4], true, left >= right)
    operation == "<" && store_or_fetch(data[4], true, left < right)
    operation == "<=" && store_or_fetch(data[4], true, left <= right)
    operation == "==" && store_or_fetch(data[4], true, left == right)
    operation == "¬=" && store_or_fetch(data[4], true, left != right)
    operation == "and" && store_or_fetch(data[4], true, left && right)
    operation == "or" && store_or_fetch(data[4], true, left || right)
    # Assignment
    operation == "<-" && store_or_fetch(data[4], true, right)
    global PointerStack[end] += 1
end

function printquad(msg_address::Union{Int64, Nothing}, last::Bool, jump::Bool=true)
    if msg_address == nothing
        message = ""
    else
        message = store_or_fetch(msg_address, false)
    end
    if msg_address ∈ ranges[3] || msg_address ∈ ranges[6] || msg_address ∈ ranges[end-1]
        message = message[2:end-1]
    end
    last || print(message, ' ')
    last && println(message)
    jump && global PointerStack[end] += 1
end

function go_to_eval(data::Vector{Any}, type::Bool)
    result = store_or_fetch(data[2], false)
    if (result && type) || (!result && !type)
        global PointerStack[end] = data[4] + 1
    else
        global PointerStack[end] += 1
    end
end

# Main
constants, modules, instructions = extract()
for constant ∈ constants
    constant[2] ∈ ranges[end-3] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end-3][1]+1), '1')
    constant[2] ∈ ranges[end-2] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end-2][1]+1), '2')
    constant[2] ∈ ranges[end-1] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end-1][1]+1), '3')
end
constants = nothing

while true
    current = instructions[PointerStack[end]]
    #println(current)
    # End runtime
    if current[1] == "EndProgram" break

    # Basic operations
    elseif current[1] ∈ operators
        operations(current, current[1])
        continue

    # I/O
    elseif current[1] == "Print"
        printquad(current[4], false)
        continue
    elseif current[1] == "LPrint"
        printquad(current[4], true)
        continue
    elseif current[1] == "Input"
        printquad(current[3], false, false)
        address = current[4]
        expected = nothing
        input = readline()
        try
            if address ∈ ranges[1] || address ∈ ranges[4] || address ∈ ranges[7] || address ∈ ranges[10]
                expected = "int"
                input = parse(Int64, input)
            elseif address ∈ ranges[2] || address ∈ ranges[5] || address ∈ ranges[8] || address ∈ ranges[11]
                expected = "float"
                input = parse(Float64, input)
            end
        catch
            @printf("Error! Type mismatch on input, expected %s.\n", expected)
            exit()
        end
        store_or_fetch(address, true, input)
        global PointerStack[end] += 1
        continue

    # Jumps
    elseif current[1] == "Goto"
        global PointerStack[end] = current[4] + 1
        continue
    elseif current[1] == "GotoF"
        go_to_eval(current, false)
        continue
    elseif current[1] == "GotoT"
        go_to_eval(current, true)
        continue

    # Modules
    elseif current[1] == "ARE"
        for fun ∈ modules
            fun[1] != current[2] && continue
            push!(Fun, fun)
        end
        for address ∈ current[3]
            try
                if store_or_fetch(address, false) !== false
                    continue
                end
            catch
                store_or_fetch(address, true, nothing)
            end
            store_or_fetch(address, true, nothing)
        end
        for address ∈ current[4]
            store_or_fetch(address, true, nothing)
        end
        global PointerStack[end] += 1
        continue
    elseif current[1] == "Parameter"
        push!(Fun, store_or_fetch(current[3], false))
        global PointerStack[end] += 1
        continue
    elseif current[1] == "GoSub"
        params = Fun[1][2]
        global Fun = Fun[2:end]
        NewMem = MemoryObj(Persistent([], [], []), Temporary([], [], [], []))
        push!(MemoryStack, NewMem)
        for i = 1:length(params)
            store_or_fetch(params[i][2], true, Fun[i])
        end
        global Fun = []
        global PointerStack[end] += 1
        push!(PointerStack, current[4] + 1)
        continue
    elseif current[1] == "Return"
        operations(current, "<-")
        pop!(MemoryStack)
        pop!(PointerStack)
        continue
    elseif current[1] == "EndModule"
        pop!(MemoryStack)
        pop!(PointerStack)
        continue
    else
        println(current)
        global PointerStack[end] += 1
        continue
    end
    break
end