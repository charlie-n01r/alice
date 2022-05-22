# Memory structures
abstract type Memory end

struct Persistent <: Memory
    type1::Vector{Union{Int64, Nothing}}
    type2::Vector{Union{Float64, Nothing}}
    type3::Vector{Union{String, Nothing}}
end

struct Temporary <: Memory
    type1::Vector{Union{Int64, Nothing}}
    type2::Vector{Union{Float64, Nothing}}
    type3::Vector{Union{Bool, Nothing}}
end

struct GlobalMem
    variables::Persistent
    constants::Persistent
end

struct MemoryObj
    persistent::Persistent
    temporary::Temporary
end

# Memory-related functions
function getMemory(mem::Memory, type::Char)
    type === '1' && return mem.type1
    type === '2' && return mem.type2
    mem.type3
end

function fetch(mem::Memory, address::UInt16, type::Char)
    memory = getMemory(mem, type)
    length(memory) === false || length(memory) < address && return false
    memory[address]
end

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
          26000:27499,
          27500:28999,
          29000:29999]

operators = ["++", "--", "^", "*", "/", "+", "-", "<", "<=", ">", ">=", "==", "¬=", "and", "or", "<-"]
