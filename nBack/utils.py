import numpy as np
import math


# trialsPerBlock      = nonTargetsPerBlock + targetsPerBlock + nbackLevel;


def create_trial_list(nback_level, total_count, trials_per_block, targets_per_block):
    trial_list = None
    n = nback_level

    num_of_blocks = math.ceil(total_count / trials_per_block)

    for block in range(num_of_blocks):

        valid_n_back_found = False
        while not valid_n_back_found:
            target_count = 0
            block_trial_list = np.zeros((2, trials_per_block))
            block_trial_list[0, :] = np.random.randint(10, size=trials_per_block)
            for position in range(block_trial_list.shape[1]):
                if position >= n:
                    if block_trial_list[0, position] == block_trial_list[0, position - n]:
                        target_count += 1
                        block_trial_list[1, position] = 1

            more_than_three = False
            for i in range(block_trial_list.shape[1] - 4):
                if block_trial_list[0, i + 1] == block_trial_list[0, i + 2] == block_trial_list[0, i + 3] == \
                        block_trial_list[0, i + 4]:
                    more_than_three = True

            if more_than_three or (target_count != targets_per_block):
                valid_n_back_found = False
            else:
                valid_n_back_found = True
                if trial_list is None:
                    trial_list = block_trial_list
                else:
                    last_index = trial_list.shape[1] - 1
                    trial_list = np.concatenate((trial_list, block_trial_list), axis=1)
                    # Check Edges
                    if trial_list[0, last_index] == trial_list[0, last_index + 1]:
                        trial_list[1, last_index + 1] = 1

    return trial_list[:, :total_count]


'''
function [trialList, levels, blocks] = nBackCreateTrialList(nBackLevel ,trialsPerBlock ,targetsPerBlock, numOfBlocks)
%Creates stimuli list for n-back task.
% Version 1.2
    
    for block      = 1:numOfBlocks

        % Counting the number of targetsPerBlock in trialListBlock
        for position = 1:length(trialListBlock)
            if position > n
                if trialListBlock(1, position) == trialListBlock(1, position - n)
                    targetCount = targetCount + 1;
                    trialListBlock(2, position) = 1;
                end
            end
        end

        % Checking whether the number of targets in trialListBlock is
        % equal to targetsPerBlock
        if targetCount ~= targetsPerBlock || moreThanThree == 1% Not equal so do it again
            
            while targetCount ~= targetsPerBlock || moreThanThree == 1
                targetCount    = 0;
                moreThanThree  = 0;
                trialListBlock(1, 1:trialsPerBlock(n)) = randi(10,1, trialsPerBlock(n));
                trialListBlock(2, 1:trialsPerBlock(n)) = zeros(1, trialsPerBlock(n));
                for position = 1:length(trialListBlock)
                    if position > n
                        if trialListBlock(1, position) == trialListBlock(1, position - n)
                            targetCount = targetCount + 1;
                            trialListBlock(2, position) = 1;
                        end
                    end
                end
                for i = 1:length(trialListBlock) - 4 % Checking whether a stimulus is repeated more than three times
                    if trialListBlock(1, i + 1) ==  trialListBlock(1, i + 2) &&  trialListBlock(1, i + 3) == trialListBlock(1, i + 1) &&  trialListBlock(1, i + 1) == trialListBlock(1, i + 4)
                        moreThanThree = 1;
                    end
                end
            end
        end
            levels    = [levels block_levels];
            blocks    = [blocks blocksBlock];
            trialList = [trialList trialListBlock];
    end
end

'''
