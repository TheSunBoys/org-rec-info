class HuffmanNode
  attr_accessor :char, :freq, :left, :right

  def initialize(char, freq)
    @char = char
    @freq = freq
    @left = nil
    @right = nil
  end
end

class HuffmanTree
  attr_reader :root

  def initialize(char_freq_map)
    @char_freq_map = char_freq_map
    @root = build_tree
  end

  def build_tree
    nodes = @char_freq_map.map { |char, freq| HuffmanNode.new(char, freq) }

    while nodes.length > 1
      nodes.sort_by! { |node| node.freq }

      left = nodes.shift
      right = nodes.shift

      merged_node = HuffmanNode.new(nil, left.freq + right.freq)
      merged_node.left = left
      merged_node.right = right

      nodes.push(merged_node)
    end

    nodes.first
  end

  def build_codes(node = @root, code = "", codes = {})
    if node.char
      codes[node.char] = code
    else
      build_codes(node.left, code + "0", codes)
      build_codes(node.right, code + "1", codes)
    end

    codes
  end
end

class UernZip
  def initialize(input_file_path)
    @input_file_path = input_file_path
    @char_freq_map = count_characters
    @huffman_tree = HuffmanTree.new(@char_freq_map)
    @codes = @huffman_tree.build_codes
  end

  def count_characters
    char_freq_map = Hash.new(0)

    File.open(@input_file_path, "r:ISO-8859-1") do |file|
      file.each_char do |char|
        char_freq_map[char] += 1
      end
    end

    char_freq_map
  end

  def compress(output_file_path)
    File.open(output_file_path, "wb") do |output_file|
      # Write number of different characters (8 bits)
      output_file.write([@char_freq_map.size].pack("C"))

      # Write character codes and their sizes
      @codes.each do |char, code|
        ascii_char = char.ord
        code_size = code.length
        output_file.write([ascii_char, code_size].pack("CS"))

        # Convert the code to binary and write to output file
        binary_code = code.to_i(2)
        output_file.write([binary_code].pack("S"))
      end

      # Write the encoded content
      encoded_content = encode_content
      output_file.write(encoded_content)

      # Add padding with zeros to complete the last byte
      padding_bits = (8 - encoded_content.length % 8) % 8
      output_file.write([0].pack("C*") * padding_bits)
    end
  end

  def encode_content
    content = File.read(@input_file_path, encoding: "ISO-8859-1")
    encoded_content = ""

    content.each_char do |char|
      encoded_content << @codes[char]
    end

    encoded_content
  end
end

class UernUnzip
  def initialize(input_file_path)
    @input_file_path = input_file_path
    @codes = {}
    @encoded_content = ""
    @num_characters = 0
  end

  def read_codes
    File.open(@input_file_path, "rb") do |input_file|
      @num_characters = input_file.read(1).unpack("C").first

      @num_characters.times do
        ascii_char, code_size = input_file.read(3).unpack("CS")
        binary_code = input_file.read(2).unpack("S").first.to_s(2).rjust(code_size, "0")
        char = ascii_char.chr("ISO-8859-1")
        @codes[binary_code] = char
      end

      @encoded_content = input_file.read
    end
  end

  def decompress(output_file_path)
    read_codes

    File.open(output_file_path, "wb") do |output_file|
      current_code = ""
      @encoded_content.each_char do |bit|
        current_code += bit

        if @codes.include?(current_code)
          char = @codes[current_code]
          output_file.write(char)
          current_code = ""
        end
      end
    end
  end
end

# Example usage:

# Compactação:
input_file_path = "poesias-margareth.txt"
output_file_path = "poesias-margareth.uzip"

uern_zip = UernZip.new(input_file_path)
uern_zip.compress(output_file_path)

# Descompactação:
input_file_path = "poesias-margareth.uzip"
output_file_path = "poesias-margareth-decompressed.txt"

uern_unzip = UernUnzip.new(input_file_path)
uern_unzip.decompress(output_file_path)
