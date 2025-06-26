format compact, clearvars, close all
%%
load carbig

%%
% range and increment for skewness
skewList = [0, 1, 2, 4,8,16,32]
kurtList = [3, 4,8,16,32,64,128,256,512,1024,2048]
leng_i=length(skewList);

fileID = fopen('exp_results.csv', 'w');
for q = 1:leng_i
    for j = 1:length(kurtList)
    
        sk = skewList(q);
        kt = kurtList(j);
        if kt > sk.^2 + 1
            moments = {0,1,sk,kt};
            rng('default');
            [r, type] = pearsrnd(moments{:}, 1000, 1);
%             try
            [Fi,xi] = ecdf(r);
            if length(Fi) == length(xi)
                len = length(Fi)
                results = [ones(len, 1) *sk, ones(len, 1) *kt, Fi, xi];
                dlmwrite('exp_results.csv', results, '-append', 'delimiter', ',', 'precision', 9)
                fprintf(fileID, '%s\n', '---Matrix End---')
            else
                continue
            end
        else
            continue
        end
    end
end
fclose(fileID)
%%