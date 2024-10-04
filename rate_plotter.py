"""
REQUIRES PYTHON 3.6 OR ABOVE!!!

VERSION 0.4
"""

import csv
import matplotlib.pyplot as plt
from matplotlib import container
from math import sqrt
from matplotlib.ticker import MultipleLocator


################# CONTROL CENTER #####################

plot_title = 'L1 Rates run 359684'
#output_file_name = 'L1test.pdf'
output_file_name = 'csvFinal/Zeroing_359684_fgb1_Sp0356_vGT.png'
display_ratio = True

# ONLY for axis label! First file rates are used as denomniator.
#ratio_wrt = 'unpacked'
ratio_wrt = 'GT emul'

# Either need to provide a file with 'L1Seeds' here or their L1Bit number in next part
import_file_for_seeds = True
L1Seeds_filename = 'L1SeedsOrdered'

# L1Bit from the rate tables to extract name in case you didn't provide a L1Seed list
L1Bits = [19,97,168,174,\
        178,189,208,210,\
        239,264,271,313,\
        343,404,421,9999]

# provide atleast as many markers as files
markers = ['o','+','x','d']

# If there is a scaling difference between rates
#scaling = [1.0, 62.2036/61.9796, 1.0, 62.2036/62.0122]
scaling = [1.0, 1.0, 1.0]

# list of all files
# if taking ratios, first file has to be the denominator rates.
files = ['csvFinal/fgbit1_Zeroing_359684_unpacked.csv',
         'csvFinal/fgbit1_NoZeroing_359684.csv',
         'csvFinal/fgbit1_Zeroing_359684.csv'
        ]

rates_cutoff = 0#500

fig_x,fig_y = 12,7
#fig_x,fig_y = 8,4

#####################################################

L1Seeds = []
if (import_file_for_seeds):
    with open(L1Seeds_filename,'r') as fp:
        for line in fp:
            line=line.strip("\n")
            L1Seeds.append(line.strip("'"))


if not L1Seeds:
    with open(files[0],'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            try:
                if line[0] == "L1Bit":
                    continue
                if int(line[0]) in L1Bits:
                    L1Seeds.append(line[1])
            except IndexError:
                pass

# image declaration here
fig, ax = plt.subplots()

if (display_ratio):
    fig, (ax, ax1) = plt.subplots(1,2, sharey=True, gridspec_kw={'width_ratios': [3, 1]})
    ax1.set_xlabel(f"Ratio to {ratio_wrt}")
    ax1.grid(True)
    rates_dict = {key: [0,0] for key in reversed(L1Seeds)} 
    ratio_dict={}

fig.suptitle(plot_title, fontsize=18)
ax.grid(True)
#ax.set_xscale('log')
ax.set_xlabel("L1 rates (Hz)")
plt.subplots_adjust(left=0.35)
#plt.subplots_adjust(left=0.20)
#fig.set_size_inches(12, 5)
fig.set_size_inches(fig_x,fig_y)

def ratio_error(list1, list2):
    rate_ratio = list2[0]/list1[0]
    ratio_error = rate_ratio * sqrt( (list1[1]/list1[0])**2 +\
            (list2[1]/list2[0])**2 )
    return([rate_ratio, ratio_error])

if(rates_cutoff):
    with open(files[0]) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            try:
                if (line[0] == 'L1Bit'):
                    continue
                if ( (float(line[3]) < rates_cutoff) and (line[1] in L1Seeds) ):
                    #print(line[1])
                    L1Seeds.remove(line[1])
            except IndexError:
                pass

for current in files:
   
    # for calculating ratios, choosing first files rates as denominator
    if (display_ratio and files.index(current)!=0):
        if (files.index(current)==1):
            denominator_rate_dict = dict(rates_dict)

        ratio_dict = dict(denominator_rate_dict)

    # rates dictionary = { L1 trigger : [ rate, error] }
    rates_dict = {key: [0,0] for key in reversed(L1Seeds)} 
    # reversing so the plot's y-axis labels are in same order as the provided list
    with open(current,'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            # Each line : 
            # [L1Bit,L1SeedName,pre-scale0,rate0,error_rate0,pure0,propotional0,Type,PAG,Comment]
            try:
                if line[1] in L1Seeds:
                    rates_dict[line[1]][0] = float(line[3]) * scaling[files.index(current)] # rates
                    rates_dict[line[1]][1] = float(line[4]) # error

                    # For some reason units of Total rate is in kHz
                    if (line[1]=='Total rate'):
                        rates_dict[line[1]] = [temp_rdr*100 for temp_rdr in rates_dict[line[1]]]

                    if (display_ratio and files.index(current)!=0):
                        ratio_dict[line[1]] = ratio_error(ratio_dict[line[1]],rates_dict[line[1]])

            except IndexError:
                print("Empty line!")

        emul = 'unpacked' if ('unpacked' in current) else \
                'emul GT' if ('NoZeroing' in current) else 'zeroing'

        #This part is for plotting data without error bars. Adjust condition accordingly.
        if (files.index(current) == 0):
            ax.plot([rate[0] for rate in rates_dict.values()] ,\
                    list(rates_dict.keys()),\
                    marker = markers[files.index(current)],\
                    label = emul,\
                    linestyle = 'None')
        #This part takes care of plots with error bars.
        else :
            ax.errorbar( [rate[0] for rate in rates_dict.values()] ,\
                    list(rates_dict.keys()),\
                    xerr = [error[1] for error in rates_dict.values()],\
                    marker = markers[files.index(current)],\
                    label = emul,\
                    linestyle = 'None',\
                    mew = 2, ms = 6 if (markers[files.index(current)] == 'd') else 8,\
                    capsize = 3)

        handles, labels = ax.get_legend_handles_labels()
        handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
        ax.legend( handles, labels)

        # this part plots the ratio plot if display_ratio is turned on.
        if (display_ratio):
            ax1.errorbar( [ratio[0] for ratio in ratio_dict.values()] ,\
                    list(ratio_dict.keys()),\
                    xerr = [error[1] for error in ratio_dict.values()],\
                    marker = markers[files.index(current)],\
                    mew = 2, ms = 6,\
                    linestyle = 'None',\
                    capsize = 3)
            ax1.set_xlim([.8,1.1])
            #ax1.set_xlim([.1,1e4])
            #ax1.set_xscale('log')
            ax1.xaxis.set_minor_locator(MultipleLocator(0.05))
            ax1.grid(which='both', linestyle='--', linewidth=0.5)


plt.savefig(output_file_name, dpi = 300)
plt.show()


