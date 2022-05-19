include("virtual_memory.jl")
using JSON, Printf

value = nothing
IP = 1
Global = GlobalMem(Persistent([], [], []), Persistent([], [], []))
Curr = MemoryObj(Persistent([], [], []), Temporary([], [], []))
MemoryStack = [Curr]

function extract()
    try
        file = open("obj.json", "r")
        input = JSON.parse(read(file, String))
        close(file)
        input["constants"], input["modules"], input["code"], input["base memory"]
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
    else
        do_store && return store(Global.constants, value, convert(UInt16, address - ranges[12][1] + 1), '3')
        fetch(Global.constants, convert(UInt16, address - ranges[12][1] + 1), '3')
    end
end

function conversion(address::Int64, value::String)
    if address ∈ ranges[1] || address ∈ ranges[4] || address ∈ ranges[7] || address ∈ ranges[10]
        return parse(Int64, value)
    elseif address ∈ ranges[2] || address ∈ ranges[5] || address ∈ ranges[8] || address ∈ ranges[11]
        return parse(Float64, value)
    elseif address ∈ ranges[9]
        return parse(Bool, value)
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
    # Assignment
    operation == "<-" && store_or_fetch(data[4], true, right)
    global IP += 1
end

function printquad(msg_address::Union{Int64, Nothing}, last::Bool, jump::Bool=true)
    if msg_address == nothing
        message = ""
    else
        message = store_or_fetch(msg_address, false)
    end
    if msg_address ∈ ranges[3] || msg_address ∈ ranges[6] || msg_address ∈ ranges[end]
        message = message[2:end-1]
    end
    last || print(message, ' ')
    last && println(message)
    jump && global IP += 1
end

function gotoEval(data::Vector{Any}, type::Bool)
    result = store_or_fetch(data[2], false)
    if (result && type) || (!result && !type)
        global IP = data[4] + 1
    else
        global IP += 1
    end
end

# Main
constants, modules, instructions, bmem = extract()
for constant ∈ constants
    constant[2] ∈ ranges[end-2] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end-2][1]+1), '1')
    constant[2] ∈ ranges[end-1] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end-1][1]+1), '2')
    constant[2] ∈ ranges[end] && store(Global.constants, constant[1], convert(UInt16, constant[2] - ranges[end][1]+1), '3')
end

while true
    current = instructions[IP]
    if current[1] == "EndProgram" break

    elseif current[1] == "Goto"
        global IP = current[4] + 1
        continue
    elseif current[1] ∈ operators
        operations(current, current[1])
        continue
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
        global value = readline()
        try
            if address ∈ ranges[1] || address ∈ ranges[4] || address ∈ ranges[7] || address ∈ ranges[10]
                expected = "int"
                global value = parse(Int64, value)
            elseif address ∈ ranges[2] || address ∈ ranges[5] || address ∈ ranges[8] || address ∈ ranges[11]
                expected = "float"
                global value = parse(Float64, value)
            end
        catch
            @printf("Error! Type mismatch on input, expected %s.\n", expected)
            exit()
        end
        store_or_fetch(address, true, value)
        IP += 1
        continue
    elseif current[1] == "GotoF"
        gotoEval(current, false)
        continue
    elseif current[1] == "GotoT"
        gotoEval(current, true)
        continue
    else
        println(current)
        global IP += 1
        continue
    end
    break
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
