from functions.get_files_info import get_files_info

def show(header, result):
    print(header)
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        print(result)

show("Result for current directory:", get_files_info("calculator", "."))
show("Result for 'pkg' directory:", get_files_info("calculator", "pkg"))
show("Result for '/bin' directory:", get_files_info("calculator", "/bin"))
show("Result for '../' directory:", get_files_info("calculator", "../"))