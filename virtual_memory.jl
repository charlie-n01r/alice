# Memory structures
abstract type Memory end

#=
    Persistent represents persistent memory, such as global variables, local
    variables and constants.
=#
struct Persistent <: Memory
    type1::Vector{Union{Int64, Nothing}}
    type2::Vector{Union{Float64, Nothing}}
    type3::Vector{Union{String, Nothing}}
end

#=
    Temporary represents all temporary variables.
=#
struct Temporary <: Memory
    type1::Vector{Union{Int64, Nothing}}
    type2::Vector{Union{Float64, Nothing}}
    type3::Vector{Union{Bool, Nothing}}
    type4::Vector{Union{UInt16, Nothing}}
end

#=
    GlobalMem represents the global memory of the virtual machine, consisting of
    global variables and all the constants.
=#
struct GlobalMem
    variables::Persistent
    constants::Persistent
end

#=
    MemoryObj represents the local memory that will go into the MemoryStack,
    which includes local persistent variables and temporary variables.
=#
struct MemoryObj
    persistent::Persistent
    temporary::Temporary
end

#=
    getMemory(mem, type):
        Given a memory instance, it will return the specific memory vector to
        modify depending on the type received.
=#
function getMemory(mem::Memory, type::Char)
    type === '1' && return mem.type1
    type === '2' && return mem.type2
    type === '3' && return mem.type3
    mem.type4
end

#=
    fetch(mem, address, type):
        Given a memory instance, an address and a type, it will attempt to fetch
        the value inside a memory array and return it.
=#
function fetch(mem::Memory, address::UInt16, type::Char)
    memory = getMemory(mem, type)
    length(memory) === false || length(memory) < address && return false
    memory[address]
end

#=
    store(mem, value, address, type):
        Given a memory instance, a value, an address and a type, it will push or
        modify the value inside a memory array that is represented by the address.
=#
function store(mem::Memory, value::Any, address::UInt16, type::Char)
    memory = getMemory(mem, type)
    if length(memory) >= address
        memory[address] = value
        return
    end
    if length(memory) + 1 == address
        push!(memory, value)
        return
    end
    while length(memory) + 1 < address
        push!(memory, nothing)
    end
    push!(memory, value)
end

# Static values
ranges = [1000:2999,
          3000:4999,
          5000:5999,
          6000:7999,
          8000:9999,
          10000:10999,
          11000:15999,
          16000:20999,
          21000:25999,
          26000:27999,
          28000:29999,
          30000:30999,
          31000:31999]

operators = ["++", "--", "^", "*", "/", "//", "+", "-", "<", "<=", ">", ">=", "==", "¬=", "and", "or", "<-", "<+>"]
stats = ["Size", "Mean", "Median", "Mode", "Variance", "Std", "Range", "Sum", "Min", "Max"]
xplots = ["Histogram", "Violin", "Box"]
xyplots = ["Bar", "Scatter"]
