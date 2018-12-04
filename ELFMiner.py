from readelf3 import *
import sys
import subprocess
from subprocess import call
import pandas as pd
import csv

features = []
headers = []

def prepare_headers():
	headers.extend(["Name", "1_Identification", "1_MachineType", "1_ELFVersion", "1_EntryPointAddress", "1_ProgramHeaderOffset", "1_SectionHeaderOffset", "1_Flags", "1_HeaderSize", "1_SizeProgramHeader", "1_EntriesProgram", "1_SizeSectionHeader", "1_EntriesSection", "1_StringTableIndex"])
	print(len(headers))
	sections_list = [".text", ".bss", ".comment", ".data", ".data1", ".debug", ".dynamic", ".dynstr", "dynsym", ".fini", ".hash", ".init", ".got", ".interp", ".line", ".note", ".plt", ".rodata", "rodata1", ".shstrtab", ".strtab", ".symtab", ".sdata", ".sbss", ".lit8", ".gptab", ".conflict", ".tdesc", ".lit4", ".reginfo", ".liblist", ".rel.dyn", ".rel.plt", ".got.plt"]

	suffix_list = ["_type", "_flags", "_size", "_table_index_link", "_info", "_alignment"]

	for i in sections_list:
		a = []
		for j in suffix_list:
			a.append(i+j)
		headers.extend(a)

	print(len(headers))

def input_file():
	file = sys.argv[1]
	features.append(file)
	print("Input file: %s" % file)
	try:
		with open(file, 'rb') as file:
			try:
				elf = ReadElf(file, sys.stdout)
				return elf
			except ELFError as ex:
				sys.stderr.write('ELF error: %s\n' % ex)
				sys.exit(1)

	except(IOError):
		print_err("IO Error when opening file")
	else:
		sys.exit(1)

	return None

def elf_headers(elf):
	identification, file_class, data, version, abi, abi_version, type_file, machine, version, entry_point_address, start_program_headers, start_section_headers, flags, header_size, size_program_header, num_program_header, size_section_header, num_section_header, str_table_ind = elf.display_file_header()
	features.extend([identification, machine, version, entry_point_address, start_program_headers, start_section_headers, flags, header_size, size_program_header, num_program_header, size_section_header, num_section_header, str_table_ind])

def section_headers(elf):
	# elf = input_file()
	sections_data_list = process(sys.argv[1])[0][1:]
	features_new = [""] * 204
	features.extend(features_new)
	for i, section_data in enumerate(sections_data_list):
		try:
			ind = headers.index(section_data[0]+"_type")
			for j, value in enumerate(section_data[1:]):
				features[ind+j] = value
		except:
			continue

def symbols_table(elf):
	file = sys.argv[1]
	dyna_st_type="NOTYPE|OBJECT|FUNC|SECTION|FILE|COMMON|SPARC_REGISTER|TLS|LOOS|HIOS|LOPROC|HIPROC"
	dyna_st_bind="LOCAL|GLOBAL|WEAK|LOOS|HIOS|LOPROC|HIPROC"
	syms = subprocess.check_output(["readelf","-s",file])
	dynS_type={'STB_LOCAL': 0, 'dynamic_s_c': 0, 'STT_NOTYPE_STB_GLOBAL': 0, 'STT_OBJECT_STB_WEAK': 0, 'STB_GLOBAL': 0, 'STB_WEAK': 0, 'STT_NOTYPE_STB_LOCAL': 0, 'STT_FUNC': 0, 'STT_FUNC_STB_GLOBAL': 0, 'STT_OBJECT_STB_GLOBAL': 0, 'STT_NOTYPE_STB_WEAK': 0, 'STT_NOTYPE': 0, 'STT_OBJECT': 0, 'STT_FUNC_STB_WEAK': 0, 'STT_FUNC_STB_LOCAL': 0, 'STT_OBJECT_STB_LOCAL': 0}
	symT_name = {'s_STB_LOCAL': 0, 'symbol_tab': 0, 's_STT_NOTYPE_STB_GLOBAL': 0, 's_STT_OBJECT_STB_WEAK': 0, 's_STB_GLOBAL': 0, 's_STB_WEAK': 0, 's_STT_NOTYPE_STB_LOCAL': 0, 's_STT_FUNC': 0, 's_STT_FUNC_STB_GLOBAL': 0, 's_STT_OBJECT_STB_GLOBAL': 0, 's_STT_NOTYPE_STB_WEAK': 0, 's_STT_NOTYPE': 0, 's_STT_OBJECT': 0, 's_STT_FUNC_STB_WEAK': 0, 's_STT_FUNC_STB_LOCAL': 0, 's_STT_OBJECT_STB_LOCAL': 0, 's_STT_OBJECT_STB_LOCAL': 0, 's_STT_SECTION_STB_LOCAL': 0, 's_STT_SECTION_STB_GLOBAL': 0}
	dynF_name={}
	symF_name = {}
	final_report = "a.txt"
	f = open(final_report, 'w')
	f.write(syms)
	f.close()

	with open(final_report,'r') as file:
		flag=0
		for line in file :
			  #print line.split()

			if len(line.split())>3 and line.split()[0]=='Symbol'and line.split()[2]=="'.dynsym'":
				count=int(line.split()[4])
				dynS_type['dynamic_s_c']=count
				flag=1
					 #print count
			if flag==1 and len(line.split())>3:
				if line.split()[3] in  dyna_st_type:
					if 'STT_'+line.split()[3] in dynS_type:
						dynS_type['STT_'+line.split()[3]]+=1
						if line.split()[3]=='FUNC':
							x=line.split()[7]
							dynF_name[x[:x.find('@')]]=1

						if line.split()[4] in dyna_st_bind:
							if 'STB_'+line.split()[4] in dynS_type:
								dynS_type['STB_'+line.split()[4]]+=1
							if 'STT_'+line.split()[3]+'_STB_'+line.split()[4] in dynS_type:
								dynS_type['STT_'+line.split()[3]+'_STB_'+line.split()[4]]+=1
			if flag==1 and len(line.split())==0:
				flag=0
			if len(line.split())>3 and line.split()[0]=='Symbol'and line.split()[2]=="'.symtab'":
				count=int(line.split()[4])
				symT_name['symbol_tab']=count
				flag = 2
			if flag == 2 and len(line.split())>3:
				if line.split()[3] in dyna_st_type:
					if 's_STT_'+line.split()[3] in symT_name:
						symT_name['s_STT_'+line.split()[3]]+=1
						if line.split()[3]=='FUNC':
							x=line.split()[7]
							symF_name[x[:x.find('@')]]=1

						if line.split()[4] in dyna_st_bind:
							if 's_STB_'+line.split()[4] in symT_name:
								symT_name['s_STB_'+line.split()[4]]+=1
							if 's_STT_'+line.split()[3]+'_STB_'+line.split()[4] in symT_name:
								symT_name['s_STT_'+line.split()[3]+'_STB_'+line.split()[4]]+=1

	for i in dynS_type.items():
		headers.append(i[0])
		features.append(i[1])
	for i in symT_name.items():
		headers.append(i[0])
		features.append(i[1])

def dynamic_section(elf):
	file = sys.argv[1]
	dynamic = subprocess.check_output(["readelf","-d", file])
	final_report = "a.txt"
	f = open(final_report, 'w')
	f.write(dynamic)
	f.close()

	dyna_name="NULL|NEEDED|PLTRELSZ|PLTGOT|HASH|STRTAB|SYMTAB|RELA|RELASZ|RELAENT|STRSZ|SYMENT|INIT|FINI|SONAME|RPATH|SYMBOLIC|REL|RELSZ|RELENT|PLTREL|DEBUG|TEXTREL|JMPREL|POSFLAG_1|BIND_NOW|INIT_ARRAY|FINI_ARRAY|INIT_ARRAYSZ|FINI_ARRAYSZ|RUNPATH|FLAGS|ENCODING|PREINIT_ARRAY|PREINIT_ARRAYSZ|MAXPOSTAGS|SUNW_AUXILIARY|SUNW_RTLDINF|SUNW_FILTER|SUNW_CAP|SUNW_SYMTAB|SUNW_SYMSZ|SUNW_ENCODING|SUNW_SORTENT|SUNW_SYMSORT|SUNW_SYMSORTSZ|SUNW_TLSSORT|SUNW_TLSSORTSZ|SUNW_CAPINFO|SUNW_STRPAD|SUNW_CAPCHAIN|SUNW_LDMACH|SUNW_CAPCHAINENT|SUNW_CAPCHAINSZ|SYMINFO|SYMINENT|SYMINSZ|VERDEF|VERDEFNUM|VERNEED|VERNEEDNUM|RELACOUNT|RELCOUNT|AUXILIARY|FILTER|CHECKSUM|MOVEENT|MOVESZ|MOVETAB|CONFIG|DEPAUDIT|AUDIT|FLAGS_1|SPARC_REGISTER"
	dynamic_name={'DYNRELAENT': 0, 'DYNRPATH': 0, 'DYNFINI': 0, 'DYNVERNEEDNUM': 0, 'DYNINIT_ARRAY': 0, 'DYNSTRSZ': 0, 'DYNSTRTAB': 0, 'DYNRELENT': 0, 'DYN': 0, 'DYNSYMTAB': 0, 'DYNFINI_ARRAYSZ': 0, 'DYNNEEDED': 0, 'DYNSYMENT': 0, 'DYNINIT': 0, 'DYNRELSZ': 0, 'DYNINIT_ARRAYSZ': 0, 'DYNVERNEED': 0, 'DYNRELASZ': 0, 'DYNREL': 0, 'DYNRELA': 0, 'DYNFINI_ARRAY': 0, 'DYNHASH': 0, 'DYNJMPREL': 0, 'DYNDEBUG': 0, 'DYNPLTGOT': 0, 'DYNNULL': 0, 'DYNPLTRELSZ': 0, 'DYNPLTREL': 0, 'VERSYM': 0, 'DYNCOUNT': 0}

	count = 0
	with open(final_report,'r') as file:
		for line in file :
			if len(line.split())>1:
				x=line.split()[1]
				x=x[1:len(x)-1]

				if x in dyna_name:
					if 'DYN'+x in dynamic_name:
						dynamic_name['DYN'+x] += 1
					count+=1

	dynamic_name['DYNCOUNT'] = count
	for i in dynamic_name.items():
		headers.append(i[0])
		features.append(i[1])
	

def write_csv():
	# print(features)
	# print(headers)
	with open("results.csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(headers)
		writer.writerow(features)

if __name__ == "__main__":
	prepare_headers()
	elf = input_file()
	elf_headers(elf)
	section_headers(elf)
	symbols_table(elf)
	dynamic_section(elf)	
	write_csv()