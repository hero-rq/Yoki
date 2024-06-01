def mystery_peace(file_path):
    try:
        with open(file_path, 'rb') as file:
            file.seek(-26, 2)
            data = bytearray(file.read(26))

        if len(data) != 26:
            raise ValueError("Error: Not enough data found in the file")

        for i in range(6, 14):
            data[i] = (data[i] - 0x5) & 0xFF
        data[14] = (data[14] + 0x3) & 0xFF

        result = data.decode('utf-8')
        return result

    except FileNotFoundError:
        print("Error: File not found")
        return None
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

mystery_file = 'mystery.png'
flag = mystery_peace(mystery_file)
if flag:
    print("Extracted Flag:", flag)
