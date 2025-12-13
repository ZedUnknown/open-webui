
<script>
    const PIXEL_COUNT = 225;
    const delay = 20; // ms between pixels
    const animationDuration = PIXEL_COUNT * delay;
    const totalCycleDuration = animationDuration * 3;
</script>

<div class="container relative w-100 h-100 bg-gray-100 dark:bg-gray-950 rounded-xl overflow-hidden shadow-lg">
    <!-- Gradient Wave -->
    <div class="gradient-wave absolute inset-0"></div>
    
    <!-- Pixels Grid -->
    <div class="absolute inset-0 grid grid-cols-15 grid-rows-15">
        {#each Array(PIXEL_COUNT) as _, i}
            <div 
                class="pixel"
                style="--delay: {i * delay}ms; --total: {totalCycleDuration}ms;"
            ></div>
        {/each}
    </div>
    
    <!-- Shimmer -->
    <div class="shimmer-wave absolute inset-0 -left-full w-full h-full"></div>
    
    <!-- Image Icon -->
    <div class="absolute inset-0 flex items-center justify-center text-gray-800 dark:text-gray-200 z-10">
        <svg class="w-20 h-20 shadow-md rounded-3xl" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="primary">
            <path d="M16.0012 7.33334C16.0012 6.62231 16.0013 6.12897 15.97 5.74545C15.9469 5.4635 15.9091 5.27399 15.8577 5.13022L15.802 5.00034C15.6481 4.69823 15.4137 4.4452 15.1262 4.26889L14.9993 4.19858C14.8413 4.11812 14.6297 4.0613 14.2542 4.03061C13.8707 3.99929 13.3771 3.99838 12.6663 3.99838H7.33325C6.62221 3.99838 6.12888 3.99928 5.74536 4.03061C5.46351 4.05364 5.27388 4.0905 5.13013 4.14194L5.00024 4.19858C4.69799 4.3526 4.44511 4.58672 4.2688 4.87436L4.19849 5.00034C4.11798 5.15834 4.06122 5.36975 4.03052 5.74545C3.99918 6.12897 3.99829 6.62231 3.99829 7.33334V11.7269L5.01782 10.7083L5.19458 10.5482C6.1104 9.80107 7.46195 9.85462 8.31567 10.7083L13.6038 15.9964C13.8548 15.9923 14.0675 15.9853 14.2542 15.9701C14.6295 15.9394 14.8413 15.8825 14.9993 15.8021L15.1262 15.7308C15.4136 15.5545 15.6481 15.3014 15.802 14.9994L15.8577 14.8695C15.9091 14.7257 15.9469 14.536 15.97 14.2542C16.0013 13.8708 16.0012 13.3772 16.0012 12.6664V7.33334ZM7.37525 11.6488C7.00846 11.282 6.42786 11.2594 6.03442 11.5804L5.95825 11.6488L4.0022 13.6048C4.00634 13.8555 4.0153 14.0678 4.03052 14.2542C4.0612 14.6298 4.11803 14.8414 4.19849 14.9994L4.2688 15.1263C4.44511 15.4137 4.69813 15.6482 5.00024 15.8021L5.13013 15.8578C5.2739 15.9092 5.46341 15.947 5.74536 15.9701C6.12888 16.0014 6.62222 16.0013 7.33325 16.0013H11.7268L7.37525 11.6488ZM13.0852 7.91635C13.085 7.3633 12.6363 6.91538 12.0833 6.91538C11.5302 6.91538 11.0815 7.3633 11.0813 7.91635C11.0813 8.46956 11.53 8.91831 12.0833 8.91831C12.6365 8.91831 13.0852 8.46956 13.0852 7.91635ZM14.4153 7.91635C14.4153 9.2041 13.371 10.2484 12.0833 10.2484C10.7955 10.2484 9.75122 9.2041 9.75122 7.91635C9.7514 6.62876 10.7956 5.5853 12.0833 5.5853C13.3709 5.5853 14.4151 6.62876 14.4153 7.91635ZM17.3313 12.6664C17.3313 13.3554 17.3319 13.9124 17.2952 14.3626C17.2624 14.7636 17.1974 15.1248 17.053 15.4613L16.9866 15.6039C16.7211 16.1248 16.3172 16.5605 15.8215 16.8646L15.6038 16.9867C15.227 17.1786 14.8206 17.2578 14.3625 17.2953C13.9123 17.332 13.3553 17.3314 12.6663 17.3314H7.33325C6.64416 17.3314 6.0872 17.332 5.63696 17.2953C5.23628 17.2625 4.87563 17.1973 4.53931 17.0531L4.39673 16.9867C3.87561 16.7211 3.43911 16.3174 3.13501 15.8216L3.01294 15.6039C2.82097 15.2271 2.74177 14.8206 2.70435 14.3626C2.66758 13.9124 2.66821 13.3553 2.66821 12.6664V7.33334C2.66821 6.64425 2.66756 6.0873 2.70435 5.63706C2.74176 5.17926 2.82113 4.77344 3.01294 4.39682L3.13501 4.17807C3.4391 3.68236 3.87569 3.27851 4.39673 3.01303L4.53931 2.94663C4.8756 2.80239 5.23632 2.73718 5.63696 2.70444C6.0872 2.66765 6.64416 2.66831 7.33325 2.66831H12.6663C13.3553 2.66831 13.9123 2.66767 14.3625 2.70444C14.8206 2.74186 15.227 2.82106 15.6038 3.01303L15.8215 3.1351C16.3174 3.4392 16.7211 3.8757 16.9866 4.39682L17.053 4.5394C17.1973 4.87572 17.2624 5.23637 17.2952 5.63706C17.332 6.0873 17.3313 6.64425 17.3313 7.33334V12.6664Z">
            </path>
        </svg>
    </div>
</div>

<style>

.container {
    background: rgba(0, 0, 0, 0.05);
    animation: pops 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

@keyframes pops {
    0% {
        transform: scale(1);
    }
    100% {
        transform: scale(1.01);
    }
}

.gradient-wave {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.08);
    background-size: 200% 200%;
    animation: gradientWave 6s ease-in-out infinite;
}

:global(.dark) .gradient-wave {
    background: rgba(255, 255, 255, 0.2);
}

@keyframes gradientWave {
    0%, 100% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
}

.shimmer-wave {
    position: absolute;
    top: 0;
    left: -150%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        110deg,
        transparent 0%,
        transparent 40%,
        rgba(255, 255, 255, 0.03) 45%,
        rgba(255, 255, 255, 0.15) 50%,
        rgba(255, 255, 255, 0.03) 55%,
        transparent 60%,
        transparent 100%
    );
    animation: shimmer 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    transform: skewX(-20deg);
}

:global(.dark) .shimmer-wave {
    background: linear-gradient(
        110deg,
        transparent 0%,
        transparent 40%,
        rgba(255, 255, 255, 0.02) 45%,
        rgba(255, 255, 255, 0.05) 50%,
        rgba(255, 255, 255, 0.02) 55%,
        transparent 60%,
        transparent 100%
    );
}

@keyframes shimmer {
    0% {
        left: -150%;
    }
    100% {
        left: 150%;
    }
}

.pixel {
    background: rgba(0, 0, 0, 0.05);
    animation: pixelWave var(--total) ease-out infinite;
    animation-delay: var(--delay);
}

@keyframes pixelWave {
    0% { 
        background: rgba(0, 0, 0, 0.1);
    }
    100% {
        background: rgba(0, 0, 0, 0.05);
    }
}
</style>